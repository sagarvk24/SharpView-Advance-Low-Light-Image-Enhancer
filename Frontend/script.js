// const viewButton = document.getElementById("viewButton");
// const enhanceButton = document.getElementById("enhanceButton");
// const imageModal = document.getElementById("imageModal");
// const modalImages = document.getElementById("modalImages");
// const closeButton = document.querySelector(".close");

// let originalImageURL = null;

// document.getElementById("imageUpload").addEventListener("change", function() {
//     const fileName = this.files[0] ? this.files[0].name : "No file chosen";
//     document.getElementById("fileName").textContent = fileName;
// });

// // Show the uploaded image on clicking "View Image"
// viewButton.addEventListener("click", () => {
//     const imageFile = document.getElementById("imageUpload").files[0];
//     if (!imageFile) {
//         alert("Please upload an image first.");
//         return;
//     }
//     originalImageURL = URL.createObjectURL(imageFile);
//     modalImages.innerHTML = `<img src="${originalImageURL}" alt="Original Image">`;
//     openModal();
// });

// // Enhance the image on clicking "Enhance Image"
// enhanceButton.addEventListener("click", async () => {
//     const imageFile = document.getElementById("imageUpload").files[0];
//     if (!imageFile) {
//         alert("Please upload an image first.");
//         return;
//     }

//     const formData = new FormData();
//     formData.append("image", imageFile);

//     try {
//         // Send the request to the Flask server
//         const response = await fetch("http://localhost:5000/enhance", {  // Update to Flask server URL
//             method: "POST",
//             body: formData
//         });

//         // Log the response status for debugging
//         console.log("Response status:", response.status);

//         const data = await response.json();
//         console.log("Response data:", data); // Log the response data for debugging

//         if (data.success) {
//             displayEnhancedImages(data.images);
//             initiateIterativeEnhancement();  // Continue the loop
//         } else {
//             alert("Image enhancement failed: " + data.message);
//         }
//     } catch (error) {
//         console.error("Error:", error);
//     }
// });

// // function displayEnhancedImages(imagePaths) {
// //     modalImages.innerHTML = "";
// //     imagePaths.forEach((path) => {
// //         const img = document.createElement("img");
// //         // Use full URL path for Flask server images
// //         img.src = `http://localhost:5000${path}`;
// //         img.alt = "Enhanced Image";
// //         modalImages.appendChild(img);
// //     });
// //     openModal();
// // }

// function openModal() {
//     imageModal.style.display = "flex";
// }

// function closeModal() {
//     imageModal.style.display = "none";
// }

// closeButton.addEventListener("click", closeModal);

// window.addEventListener("click", (e) => {
//     if (e.target === imageModal) {
//         closeModal();
//     }
// });


// // Function to fetch and display all images
// async function fetchAllImages() {
//     try {
//         const response = await fetch("http://localhost:5000/images");
//         const data = await response.json();

//         if (data.success) {
//             displayImages(data.images);
//         } else {
//             alert("Failed to retrieve images: " + data.message);
//         }
//     } catch (error) {
//         console.error("Error fetching images:", error);
//     }
// }

// // function displayEnhancedImages(imagePaths) {
// //     modalImages.innerHTML = "";
// //     imagePaths.forEach((path) => {
// //         const img = document.createElement("img");
// //         // Use the server route to access images in the enhanced folder
// //         const filename = path.split('/').pop(); // Extract filename from path
// //         img.src = `http://localhost:5000/images/${filename}`;
// //         img.alt = "Enhanced Image";
// //         img.style.width = "100%";
// //         img.style.height = "auto";
// //         modalImages.appendChild(img);
// //     });
// //     openModal();
// // }


// function displayEnhancedImages(imagePaths) {
//     modalImages.innerHTML = ""; // Clear previous images
//     const imageLabels = ["Original Image", "Gamma Image", "Gaussian Image", "Gray World Image"]; // Define the labels

//     imagePaths.forEach((path, index) => {
//         // Create an image element
//         const img = document.createElement("img");
//         const filename = path.split('/').pop(); // Extract filename from path
//         img.src = `http://localhost:5000/images/${filename}`; // Server path to access images
//         img.alt = "Enhanced Image";
//         img.style.width = "100%";
//         img.style.height = "auto";

//         // Create a label element
//         const labelElement = document.createElement("div");
//         labelElement.classList.add("image-label"); // Add a class for styling
//         labelElement.innerText = imageLabels[index] || "Enhanced Image"; // Use label based on index

//         // Create a wrapper div to contain both the image and label
//         const imageWrapper = document.createElement("div");
//         imageWrapper.classList.add("image-wrapper"); // Add a class for styling the wrapper
//         imageWrapper.appendChild(img);
//         imageWrapper.appendChild(labelElement);

//         // Append the wrapper to modal images
//         modalImages.appendChild(imageWrapper);
//     });

//     openModal(); // Ensure the modal opens after images are added
// }


// // Call fetchAllImages function when needed
// // For example, you could call it on button click or when the page loads
// document.getElementById("yourButtonId").addEventListener("click", fetchAllImages);


// async function initiateIterativeEnhancement() {
//     setTimeout(async () => {  // 12-second delay before prompting
//         const furtherEnhancement = confirm("Do you wish to enhance the image further?");
//         if (!furtherEnhancement) return;

//         const brightness = prompt("Enter the brightness value (0-50):");
//         if (brightness === null || brightness === "") return;

//         try {
//             const response = await fetch(`http://localhost:5000/iterative_enhance?brightness=${brightness}`);
//             const data = await response.json();

//             if (data.success) {
//                 const newImage = data.image;
//                 modalImages.innerHTML = `<img src="http://localhost:5000${newImage}" alt="Enhanced Image">`;
//                 initiateIterativeEnhancement();  // Recursively call for the next iteration
//             } else {
//                 alert("Enhancement failed: " + data.message);
//             }
//         } catch (error) {
//             console.error("Error:", error);
//         }
//     }, 5000); // 5-second delay between each iteration
// }

const viewButton = document.getElementById("viewButton");
const enhanceButton = document.getElementById("enhanceButton");
const imageModal = document.getElementById("imageModal");
const modalImages = document.getElementById("modalImages");
const closeButton = document.querySelector(".close");

let originalImageURL = null;

// Display the chosen file name when an image is uploaded
document.getElementById("imageUpload").addEventListener("change", function () {
    const fileName = this.files[0] ? this.files[0].name : "No file chosen";
    document.getElementById("fileName").textContent = fileName;
});

// Show the uploaded image on clicking "View Image"
viewButton.addEventListener("click", () => {
    const imageFile = document.getElementById("imageUpload").files[0];
    if (!imageFile) {
        alert("Please upload an image first.");
        return;
    }
    originalImageURL = URL.createObjectURL(imageFile);
    modalImages.innerHTML = `<img src="${originalImageURL}" alt="Original Image">`;
    openModal();
});

// Enhance the image on clicking "Enhance Image"
enhanceButton.addEventListener("click", async () => {
    const imageFile = document.getElementById("imageUpload").files[0];
    if (!imageFile) {
        alert("Please upload an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("image", imageFile);

    try {
        const response = await fetch("http://localhost:5000/enhance", { // Flask server URL
            method: "POST",
            body: formData
        });

        console.log("Response status:", response.status);

        const data = await response.json();
        console.log("Response data:", data);

        if (data.success) {
            displayEnhancedImages(data.images); // Display the first set of enhancements
            initiateIterativeEnhancement(); // Start the iterative enhancement process
        } else {
            alert("Image enhancement failed: " + data.message);
        }
    } catch (error) {
        console.error("Error:", error);
    }
});

function openModal() {
    imageModal.style.display = "flex";
}

function closeModal() {
    imageModal.style.display = "none";
}

closeButton.addEventListener("click", closeModal);

window.addEventListener("click", (e) => {
    if (e.target === imageModal) {
        closeModal();
    }
});

// Function to dynamically display enhanced images
function displayEnhancedImages(imagePaths) {
    modalImages.innerHTML = "";
    const imageLabels = ["Original Image", "Gamma Image", "Gaussian Image", "Gray World Image"];
    imagePaths.forEach((path, index) => 
    {
        const img = document.createElement("img");
        img.src = `http://localhost:5000/images/${path.split('/').pop()}`;
        img.alt = "Enhanced Image";
        img.style.width = "100%";
        img.style.height = "auto";

        const label = document.createElement("div");
        label.classList.add("image-label");
        label.innerText = imageLabels[index] || "Enhanced Image";

        const wrapper = document.createElement("div");
        wrapper.classList.add("image-wrapper");
        wrapper.appendChild(img);
        wrapper.appendChild(label);

        modalImages.appendChild(wrapper);
    });
    openModal();
}

// // Function to handle iterative enhancement
// async function initiateIterativeEnhancement() {
//     let inputPath = "output_gamma.jpeg"; // Initial input file
//     const outputPath = "iterative_output.jpeg"; // Output file for each iteration

//     setTimeout(async () => {
//         const furtherEnhancement = confirm("Do you wish to enhance the image further?");
//         if (!furtherEnhancement) return;

//         const brightness = prompt("Enter the brightness value (0-50):");
//         if (!brightness) return;

//         try {
//             const response = await fetch(
//                 `http://localhost:5000/iterative_enhance?brightness=${brightness}&input=${inputPath}&output=${outputPath}`
//             );

//             const data = await response.json();

//             if (data.success) 
//             {
//                 inputPath = data.output; // Update input for next iteration
//                 updateEnhancedImage(data.output); // Display the enhanced image
//                 initiateIterativeEnhancement(); // Recursive call
//             } 
            
//             else {
//                 alert("Enhancement failed: " + data.message);
//             }
//         } 
//         catch (error) 
//         {
//             console.error("Error:", error);
//         }
//     }, 5000); // 5-second delay
// }


async function initiateIterativeEnhancement() {
    let inputPath = "output_gamma.jpeg"; // Initial input image
    const outputPath = "iterative_output.jpeg"; // Iterative output image path

    setTimeout(async () => {
        const furtherEnhancement = confirm("Do you wish to enhance the image further?");
        if (!furtherEnhancement) return; // End process if user cancels

        const brightness = prompt("Enter the brightness value (0-50):");
        if (!brightness) return; // Exit if no value is provided

        try {
            const response = await fetch(
                `http://localhost:5000/iterative_enhance?brightness=${brightness}&input=${inputPath}&output=${outputPath}`
            );
            const data = await response.json();

            if (data.success) {
                // Update inputPath for the next iteration
                inputPath = outputPath;

                // Dynamically update the enhanced image in the 'enhancedBox'
                updateEnhancedImage(data.image);

                // Recursive call for further enhancement
                initiateIterativeEnhancement();
            } else {
                alert("Enhancement failed: " + data.message);
            }
        } catch (error) {
            console.error("Error during iterative enhancement:", error);
        }
    }, 5000); // 5-second delay before prompting for the next iteration
}

function updateEnhancedImage(imagePath) {
    const enhancedBox = document.getElementById("enhancedBox");
    console.log("Updating enhancedBox with image:", imagePath); // Debugging log
    enhancedBox.innerHTML = `<img src="http://localhost:5000${imagePath}" alt="Enhanced Image">`;
}

const enhancedBox = document.getElementById("enhancedBox");
const closeEnhancedBox = document.querySelector(".closeEnhancedBox");

// Function to show the Enhanced Box
function showEnhancedBox(content) {
    enhancedBox.style.display = "flex"; // Show the box
    enhancedBox.innerHTML = `
        <span class="closeEnhancedBox">&times;</span>
        ${content} <!-- Dynamically added content -->
    `;
    addCloseEnhancedBoxEvent();
}

// Function to hide the Enhanced Box
function hideEnhancedBox() {
    enhancedBox.style.display = "none"; // Hide the box
}

// Add close functionality
function addCloseEnhancedBoxEvent() {
    const closeEnhancedBox = document.querySelector(".closeEnhancedBox");
    if (closeEnhancedBox) {
        closeEnhancedBox.addEventListener("click", hideEnhancedBox);
    }
}

// Add click event for background closing
window.addEventListener("click", (e) => {
    if (e.target === enhancedBox) {
        hideEnhancedBox();
    }
});



