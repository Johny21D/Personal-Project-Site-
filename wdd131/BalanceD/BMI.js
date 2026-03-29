// ─── 1. ARRAYS of meal and workout options ───────────────────────────────────
// Each item has a "category" so we can filter by BMI result

const meals = [
    { name: "Oatmeal with berries",      category: "underweight", emoji: "🥣" },
    { name: "Peanut butter banana wrap", category: "underweight", emoji: "🌯" },
    { name: "Greek yogurt with granola", category: "underweight", emoji: "🥛" },
    { name: "Avocado toast with eggs",   category: "underweight", emoji: "🍳" },

    { name: "Grilled chicken salad",     category: "normal",      emoji: "🥗" },
    { name: "Brown rice and veggies",    category: "normal",      emoji: "🍚" },
    { name: "Turkey sandwich",           category: "normal",      emoji: "🥪" },
    { name: "Salmon with quinoa",        category: "normal",      emoji: "🐟" },

    { name: "Veggie stir fry",           category: "overweight",  emoji: "🥦" },
    { name: "Grilled fish with salad",   category: "overweight",  emoji: "🐠" },
    { name: "Lentil soup",               category: "overweight",  emoji: "🍲" },
    { name: "Cucumber and hummus",       category: "overweight",  emoji: "🥒" },

    { name: "Green smoothie",            category: "obese",       emoji: "🥤" },
    { name: "Boiled eggs and veggies",   category: "obese",       emoji: "🥚" },
    { name: "Mixed greens salad",        category: "obese",       emoji: "🥬" },
    { name: "Steamed broccoli & chicken",category: "obese",       emoji: "🍗" },
];

const workouts = [
    { name: "Weight training",           category: "underweight", emoji: "🏋️" },
    { name: "Resistance band exercises", category: "underweight", emoji: "💪" },
    { name: "Yoga for strength",         category: "underweight", emoji: "🧘" },
    { name: "Swimming",                  category: "underweight", emoji: "🏊" },

    { name: "30-min jog",                category: "normal",      emoji: "🏃" },
    { name: "Cycling",                   category: "normal",      emoji: "🚴" },
    { name: "Jump rope",                 category: "normal",      emoji: "🪢" },
    { name: "HIIT circuit",              category: "normal",      emoji: "⚡" },

    { name: "Brisk walking",             category: "overweight",  emoji: "🚶" },
    { name: "Light jogging",             category: "overweight",  emoji: "👟" },
    { name: "Water aerobics",            category: "overweight",  emoji: "💧" },
    { name: "Beginner yoga",             category: "overweight",  emoji: "🧘" },

    { name: "Daily 20-min walk",         category: "obese",       emoji: "🌿" },
    { name: "Chair exercises",           category: "obese",       emoji: "🪑" },
    { name: "Gentle stretching",         category: "obese",       emoji: "🤸" },
    { name: "Low-impact aerobics",       category: "obese",       emoji: "❤️" },
];


// ─── 2. Gender toggle buttons ─────────────────────────────────────────────────

const genderButtons = document.querySelectorAll(".gender-btn");
let selectedGender = "male"; // default

genderButtons.forEach(function(btn) {
    btn.addEventListener("click", function() {
        // Remove active from all buttons
        genderButtons.forEach(function(b) { b.classList.remove("active"); });
        // Add active to the clicked one
        btn.classList.add("active");
        selectedGender = btn.dataset.gender;
    });
});


// ─── 3. Form submit ───────────────────────────────────────────────────────────

const form = document.getElementById("bmi-form");

form.addEventListener("submit", function(e) {
    e.preventDefault(); // stop page from refreshing

    // --- Capture form data into a structured OBJECT ---
    const userInfo = {
        weight: parseFloat(document.getElementById("weight").value),
        height: parseFloat(document.getElementById("height").value),
        age:    parseInt(document.getElementById("age").value),
        gender: selectedGender,
    };

    // --- Calculate BMI ---
    const heightInMeters = userInfo.height / 100;
    const bmi = userInfo.weight / (heightInMeters * heightInMeters);
    const bmiRounded = Math.round(bmi * 10) / 10;

    // --- Determine category ---
    let category = "";
    if (bmi < 18.5) {
        category = "underweight";
    } else if (bmi < 25) {
        category = "normal";
    } else if (bmi < 30) {
        category = "overweight";
    } else {
        category = "obese";
    }

    // --- Show BMI number and label ---
    document.getElementById("bmi-value").textContent = bmiRounded;
    document.getElementById("bmi-category").textContent =
        category.charAt(0).toUpperCase() + category.slice(1);

    // --- Move the indicator bar ---
    // BMI scale: 15 (left edge) to 40 (right edge)
    let percent = ((bmiRounded - 15) / (40 - 15)) * 100;
    if (percent < 2)   percent = 2;
    if (percent > 98)  percent = 98;
    document.getElementById("bmi-indicator").style.left = percent + "%";

    // --- Show the results panel ---
    const resultsPanel = document.getElementById("results-panel");
    resultsPanel.classList.add("visible");

    // --- Generate recommendations ---
    showRecommendations(category);
});

function showRecommendations(category) {

    // FILTER — keep only items that match the user's category
    const filteredMeals    = meals.filter(function(item) {
        return item.category === category;
    });

    const filteredWorkouts = workouts.filter(function(item) {
        return item.category === category;
    });

    // MAP — turn each filtered item into an HTML list item string
    const mealItems = filteredMeals.map(function(item) {
        return `<li>${item.emoji} ${item.name}</li>`;
    });

    const workoutItems = filteredWorkouts.map(function(item) {
        return `<li>${item.emoji} ${item.name}</li>`;
    });

    // BUILD the two cards as HTML strings
    const cardsHTML = `
        <div class="recommendation-grid">
            <div class="rec-card">
                <h4>🥗 Meal Suggestions</h4>
                <ul>
                    ${mealItems.join("")}
                </ul>
            </div>
            <div class="rec-card">
                <h4>🏃 Workout Suggestions</h4>
                <ul>
                    ${workoutItems.join("")}
                </ul>
            </div>
        </div>
    `;

    // INJECT into the page via DOM
    document.getElementById("ai-output").innerHTML = cardsHTML;
}