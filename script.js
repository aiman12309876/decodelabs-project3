document.addEventListener("DOMContentLoaded", function () {

    // ========== 1. Button Click ==========
    const clickBtn = document.getElementById("clickBtn");
    const clickMessage = document.getElementById("clickMessage");

    clickBtn.addEventListener("click", function () {
        clickMessage.textContent = "🎉 You clicked the button! Good job!";
        clickMessage.style.color = "#00d4ff";
    });

    // ========== 2. Dark Mode Toggle ==========
    const darkModeBtn = document.getElementById("darkModeBtn");
    let isDarkMode = false;

    darkModeBtn.addEventListener("click", function () {
        isDarkMode = !isDarkMode;
        document.body.classList.toggle("dark-mode");
        darkModeBtn.textContent = isDarkMode ? "Light Mode" : "Dark Mode";
    });

    // ========== 3. Counter ==========
    let count = 0;
    const counterDisplay = document.getElementById("counterDisplay");
    const increaseBtn = document.getElementById("increaseBtn");
    const decreaseBtn = document.getElementById("decreaseBtn");

    increaseBtn.addEventListener("click", function () {
        count++;
        counterDisplay.textContent = count;
    });

    decreaseBtn.addEventListener("click", function () {
        count--;
        counterDisplay.textContent = count;
    });

    // ========== 4. Show / Hide ==========
    const toggleBtn = document.getElementById("toggleBtn");
    const toggleText = document.getElementById("toggleText");
    let isVisible = true;

    toggleBtn.addEventListener("click", function () {
        isVisible = !isVisible;
        toggleText.classList.toggle("hidden");
        toggleBtn.textContent = isVisible ? "Hide" : "Show";
    });

    // ========== 5. Image Gallery ==========
    const galleryImage = document.getElementById("galleryImage");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let imageIndex = 1;

    function updateImage() {
        galleryImage.src = "https://picsum.photos/200/150?random=" + imageIndex;
    }

    nextBtn.addEventListener("click", function () {
        imageIndex++;
        updateImage();
    });

    prevBtn.addEventListener("click", function () {
        if (imageIndex > 1) {
            imageIndex--;
            updateImage();
        } else {
            alert("This is the first image!");
        }
    });

    // ========== 6. Color Changer ==========
    const colorBox = document.getElementById("colorBox");
    const colorBtn = document.getElementById("colorBtn");

    const colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c", "#e67e22"];

    colorBtn.addEventListener("click", function () {
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        colorBox.style.background = randomColor;
    });

});