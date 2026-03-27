
    /* ── Gender toggle ── */
    let selectedGender = 'male';
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedGender = btn.dataset.gender;
        });
    });

    /* ── BMI calculation helpers ── */
    function calcBMI(weight, height) {
        const hm = height / 100;
        return (weight / (hm * hm)).toFixed(1);
    }

    function getCategory(bmi) {
        if (bmi < 18.5) return 'Underweight';
        if (bmi < 25)   return 'Normal Weight';
        if (bmi < 30)   return 'Overweight';
        return 'Obese';
    }

    /* Maps BMI to % position on the gradient bar (18.5 → 0%, 40 → 100%) */
    function bmiToPercent(bmi) {
        const min = 15, max = 40;
        return Math.min(100, Math.max(0, ((bmi - min) / (max - min)) * 100));
    }

    /* ── Claude API call ── */
    async function fetchRecommendations(weight, height, age, gender, bmi, category) {
        const prompt = `You are a certified nutritionist and personal trainer. A user has submitted their health data:
- Age: ${age}
- Gender: ${gender}
- Weight: ${weight} kg
- Height: ${height} cm
- BMI: ${bmi} (${category})

Respond ONLY with a valid JSON object — no markdown, no extra text. Use this exact structure:
{
  "summary": "One motivating sentence about their health status.",
  "foods_to_eat": ["item 1", "item 2", "item 3", "item 4", "item 5"],
  "foods_to_avoid": ["item 1", "item 2", "item 3", "item 4"],
  "meal_timing": ["tip 1", "tip 2", "tip 3"],
  "exercises": ["exercise 1", "exercise 2", "exercise 3", "exercise 4"],
  "weekly_goal": "One specific, achievable weekly health goal."
}`;

        const response = await fetch("https://api.anthropic.com/v1/messages", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "claude-sonnet-4-20250514",
                max_tokens: 1000,
                messages: [{ role: "user", content: prompt }]
            })
        });

        const data = await response.json();
        const rawText = data.content.map(b => b.text || "").join("");
        return JSON.parse(rawText.replace(/```json|```/g, "").trim());
    }

    /* ── Render recommendations ── */
    function renderRecommendations(rec) {
        return `
        <p style="color:var(--text-muted);margin-bottom:20px;font-size:0.95rem;line-height:1.6;">
            ${rec.summary}
        </p>
        <div class="recommendation-grid">
            <div class="rec-card">
                <h4>🥗 Foods to Eat</h4>
                <ul>${rec.foods_to_eat.map(f => `<li>${f}</li>`).join("")}</ul>
            </div>
            <div class="rec-card">
                <h4>🚫 Foods to Limit</h4>
                <ul>${rec.foods_to_avoid.map(f => `<li>${f}</li>`).join("")}</ul>
            </div>
            <div class="rec-card">
                <h4>⏰ Meal Timing</h4>
                <ul>${rec.meal_timing.map(t => `<li>${t}</li>`).join("")}</ul>
            </div>
            <div class="rec-card">
                <h4>🏃 Exercises</h4>
                <ul>${rec.exercises.map(e => `<li>${e}</li>`).join("")}</ul>
            </div>
        </div>
        <div style="margin-top:20px;padding:16px 20px;background:linear-gradient(135deg,#e8f5e9,#f1f8e9);border-radius:10px;border-left:4px solid var(--green-mid);">
            <strong style="font-size:0.8rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--green-dark);">🎯 Weekly Goal</strong>
            <p style="margin-top:6px;color:var(--text-main);font-size:0.93rem;line-height:1.5;">${rec.weekly_goal}</p>
        </div>`;
    }

    /* ── Form submit ── */
    document.getElementById('bmi-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);
        const age    = parseInt(document.getElementById('age').value);
        const gender = selectedGender;

        if (!weight || !height || !age) return;

        const bmi      = calcBMI(weight, height);
        const category = getCategory(parseFloat(bmi));

        /* Show BMI badge */
        document.getElementById('bmi-value').textContent    = bmi;
        document.getElementById('bmi-category').textContent = category;
        document.getElementById('bmi-indicator').style.left = bmiToPercent(parseFloat(bmi)) + '%';

        /* Show panel with loading */
        const panel = document.getElementById('results-panel');
        panel.classList.add('visible');
        document.getElementById('ai-output').innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <span>Generating your personalized plan…</span>
            </div>`;

        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });

        /* Disable button */
        const btn = document.getElementById('calc-btn');
        btn.disabled = true;
        btn.textContent = 'Calculating…';

        try {
            const rec = await fetchRecommendations(weight, height, age, gender, bmi, category);
            document.getElementById('ai-output').innerHTML = renderRecommendations(rec);
        } catch (err) {
            document.getElementById('ai-output').innerHTML = `
                <div class="error-msg">
                    ⚠️ Could not load recommendations right now. Please try again in a moment.
                </div>`;
        } finally {
            btn.disabled = false;
            btn.textContent = 'Calculate BMI & Get Recommendations';
        }
    });


