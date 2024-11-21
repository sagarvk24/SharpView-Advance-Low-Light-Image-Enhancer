#include <iostream> // Input/output operations
#include <fstream>  // File operations
#include <vector>   // Dynamic arrays
#include <string>
#include <algorithm> // Sort, STL functions
#include <cmath>     // For exp() in Gaussian function
using namespace std;

template <typename T>
T clamp(T value, T low, T high)
{
    return (value < low) ? low : (value > high) ? high
                                                : value;
}

// Structure to represent a pixel with RGB values
struct Pixel
{
    unsigned char r, g, b;
};

// Function to read a PPM image file
bool readPPM(const string &filename, vector<Pixel> &image, int &width, int &height)
{
    ifstream file(filename, ios::binary);
    if (!file)
    {
        cerr << "Error opening file: " << filename << endl;
        return false;
    }

    string magicNumber;
    file >> magicNumber;
    if (magicNumber != "P6")
    {
        cerr << "Unsupported file format: " << magicNumber << endl;
        return false;
    }

    file >> width >> height;
    int maxColorValue;
    file >> maxColorValue;
    file.get(); // Consume the newline after maxColorValue

    image.resize(width * height);
    file.read(reinterpret_cast<char *>(image.data()), width * height * 3); // Read pixel data
    file.close();
    return true;
}

// Function to write a PPM image file
bool writePPM(const string &filename, const vector<Pixel> &image, int width, int height)
{
    ofstream file(filename, ios::binary);
    if (!file)
    {
        cerr << "Error opening file: " << filename << endl;
        return false;
    }

    file << "P6\n"
         << width << " " << height << "\n255\n";                                  // Write the header
    file.write(reinterpret_cast<const char *>(image.data()), width * height * 3); // Write pixel data
    file.close();
    return true;
}

// Function to generate a Gaussian kernel
vector<vector<double>> generateGaussianKernel(int kernelSize, double sigma)
{
    int halfSize = kernelSize / 2;
    vector<vector<double>> kernel(kernelSize, vector<double>(kernelSize));
    double sum = 0.0;

    // Compute the Gaussian kernel
    for (int i = -halfSize; i <= halfSize; ++i)
    {
        for (int j = -halfSize; j <= halfSize; ++j)
        {
            kernel[i + halfSize][j + halfSize] = (1 / (2 * M_PI * sigma * sigma)) * exp(-(i * i + j * j) / (2 * sigma * sigma));
            sum += kernel[i + halfSize][j + halfSize];
        }
    }

    // Normalize the kernel
    for (int i = 0; i < kernelSize; ++i)
    {
        for (int j = 0; j < kernelSize; ++j)
        {
            kernel[i][j] /= sum;
        }
    }

    return kernel;
}

// Function to apply Gaussian smoothing to an image
void applyGaussianSmoothing(vector<Pixel> &image, int width, int height, int kernelSize, double sigma)
{
    vector<Pixel> tempImage = image; // Make a copy of the original image

    vector<vector<double>> kernel = generateGaussianKernel(kernelSize, sigma);
    int halfKernel = kernelSize / 2;

    // Iterate over every pixel in the image
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
            double rSum = 0, gSum = 0, bSum = 0;

            // Apply the Gaussian kernel
            for (int ky = -halfKernel; ky <= halfKernel; ++ky)
            {
                for (int kx = -halfKernel; kx <= halfKernel; ++kx)
                {
                    // Calculate the position of the neighboring pixel
                    int px = min(max(x + kx, 0), width - 1);  // Ensure the index is within the image boundaries
                    int py = min(max(y + ky, 0), height - 1); // Handle edges

                    int pixelIndex = py * width + px;

                    // Accumulate weighted sums for each channel
                    rSum += kernel[ky + halfKernel][kx + halfKernel] * tempImage[pixelIndex].r;
                    gSum += kernel[ky + halfKernel][kx + halfKernel] * tempImage[pixelIndex].g;
                    bSum += kernel[ky + halfKernel][kx + halfKernel] * tempImage[pixelIndex].b;
                }
            }

            // Assign the new pixel value
            image[y * width + x].r = static_cast<unsigned char>(min(255.0, max(0.0, rSum)));
            image[y * width + x].g = static_cast<unsigned char>(min(255.0, max(0.0, gSum)));
            image[y * width + x].b = static_cast<unsigned char>(min(255.0, max(0.0, bSum)));
        }
    }
}

// Gamma Correction Function
vector<Pixel> applyGammaCorrection(const vector<Pixel> &image, int width, int height, float gamma)
{
    vector<Pixel> correctedImage = image;

    // Ensure gamma is positive
    if (gamma <= 0)
    {
        cerr << "Gamma value should be positive." << endl;
        return correctedImage; // Return the original image if gamma is invalid
    }

    // Precompute the gamma table to speed up the process
    const int maxColorValue = 255;
    vector<unsigned char> gammaTable(maxColorValue + 1);
    float inverseGamma = 0.85f / gamma;
    for (int i = 0; i <= maxColorValue; ++i)
    {
        // Compute gamma-corrected value and clamp it between 0 and 255
        gammaTable[i] = static_cast<unsigned char>(clamp(pow(i / 255.0f, inverseGamma) * 255.0f, 0.0f, 255.0f));
    }

    // Apply gamma correction using the precomputed table
    for (auto &pixel : correctedImage)
    {
        pixel.r = gammaTable[pixel.r];
        pixel.g = gammaTable[pixel.g];
        pixel.b = gammaTable[pixel.b];
    }

    return correctedImage;
}

// Function to apply Gray World Color Balance
void applyGrayWorldBalance(vector<Pixel> &image, int width, int height)
{
    double rSum = 0, gSum = 0, bSum = 0;
    int totalPixels = width * height;

    // Calculate the average RGB values
    for (const auto &pixel : image)
    {
        rSum += pixel.r;
        gSum += pixel.g;
        bSum += pixel.b;
    }

    double avgR = rSum / totalPixels;
    double avgG = gSum / totalPixels;
    double avgB = bSum / totalPixels;

    // Calculate the scale factors to balance the colors
    double scaleR = avgG / avgR;
    double scaleG = avgG / avgG; // This will always be 1
    double scaleB = avgG / avgB;

    // Apply the scale factors to each pixel
    for (auto &pixel : image)
    {
        pixel.r = static_cast<unsigned char>(clamp(pixel.r * scaleR, 0.0, 255.0));
        pixel.g = static_cast<unsigned char>(clamp(pixel.g * scaleG, 0.0, 255.0));
        pixel.b = static_cast<unsigned char>(clamp(pixel.b * scaleB, 0.0, 255.0));
    }
}

// Function to adjust brightness
void adjustBrightness(vector<Pixel> &image, int width, int height, int value)
{
    for (auto &pixel : image)
    {
        pixel.r = static_cast<unsigned char>(clamp(pixel.r + value, 0, 255));
        pixel.g = static_cast<unsigned char>(clamp(pixel.g + value, 0, 255));
        pixel.b = static_cast<unsigned char>(clamp(pixel.b + value, 0, 255));
    }
}

// Function to adjust contrast
void adjustContrast(vector<Pixel> &image, int width, int height, float factor)
{
    const int midpoint = 128;
    for (auto &pixel : image)
    {
        pixel.r = static_cast<unsigned char>(clamp(midpoint + factor * (pixel.r - midpoint), 0.0f, 255.0f));
        pixel.g = static_cast<unsigned char>(clamp(midpoint + factor * (pixel.g - midpoint), 0.0f, 255.0f));
        pixel.b = static_cast<unsigned char>(clamp(midpoint + factor * (pixel.b - midpoint), 0.0f, 255.0f));
    }
}


int main()
{
    string inputFilename = "image.ppm";
    // cout << "Enter input PPM image filename: ";
    // cin >> inputFilename;
    string gammaOutputFilename = "output_gamma.ppm";
    string grayWorldOutputFilename = "output_grayworld.ppm";
    string gaussianFileName = "output_gaussian.ppm";
    string outputFileName = "enhancedOutput.ppm";

    vector<Pixel> image;
    int width, height;

    if (!readPPM(inputFilename, image, width, height))
    {
        return -1;
    }

    vector<Pixel> gaussianImage = image;

    applyGaussianSmoothing(gaussianImage, width, height, 3, 0.8);

    // Save the Gaussian Smoothing output image
    if (!writePPM(gaussianFileName, gaussianImage, width, height))
    {
        return -1;
    }
    cout << "Gaussian Smoothing applied and saved to " << gaussianFileName << endl;

    float gamma = 1.4f; // Gamma value for Gamma Correction

    vector<Pixel> gammImage = gaussianImage;

    // Apply Gamma Correction
    vector<Pixel> gammaImage = applyGammaCorrection(gammImage, width, height, gamma);

    // Save the Gamma Correction output image
    if (!writePPM(gammaOutputFilename, gammaImage, width, height))
    {
        return -1;
    }
    cout << "Gamma Correction applied and saved to " << gammaOutputFilename << endl;

    // Apply Gray World Color Balance
    applyGrayWorldBalance(gammaImage, width, height);

    // Save the Gray World output image
    if (!writePPM(grayWorldOutputFilename, gammaImage, width, height))
    {
        return -1;
    }
    cout << "Gray World Color Balance applied and saved to " << grayWorldOutputFilename << endl;

    float contrastFactor = 1.2f; // Reduce contrast
    int brightnessValue;
    bool keepEnhancing  = true;

    do
    {
        int choice;
        cout << "Do you wish to enhnace the image further? (Yes = 1 / No = 2): ";
        cin >> choice;
        switch (choice)
        {
        case 1:
            // Brightness adjustment

            cout << "Enter the value for increasing brightness (0-50): ";
            cin >> brightnessValue;
            adjustBrightness(gammaImage, width, height, brightnessValue);
            adjustContrast(gammaImage, width, height, contrastFactor);

            // Save the enhanced image
            if (!writePPM("enhancedOutput.ppm", gammaImage, width, height))
            {
                cerr << "Error saving enhanced image." << endl;
                return -1;
            }
            cout << "Enhanced image saved as"<<outputFileName << endl;
            break;

        case 2:
            keepEnhancing = false;
            break;

        default:
            cout << "Wrong Choice";
        }

    } while (keepEnhancing);

    return 0;
}