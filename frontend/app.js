(function () {
  "use strict";

  const API_BASE = "http://localhost:8000";

  const form = document.getElementById("content-form");
  const submitBtn = document.getElementById("submit-btn");
  const loading = document.getElementById("loading");
  const errorEl = document.getElementById("error");
  const errorMessage = document.getElementById("error-message");
  const results = document.getElementById("results");
  const resultsBusiness = document.getElementById("results-business");
  const postsContainer = document.getElementById("posts-container");

  function show(el) {
    el.classList.remove("hidden");
    el.setAttribute("aria-hidden", "false");
  }

  function hide(el) {
    el.classList.add("hidden");
    el.setAttribute("aria-hidden", "true");
  }

  function setLoading(active) {
    if (active) {
      hide(errorEl);
      hide(results);
      show(loading);
      submitBtn.disabled = true;
    } else {
      hide(loading);
      submitBtn.disabled = false;
    }
  }

  function showError(message) {
    hide(loading);
    submitBtn.disabled = false;
    errorMessage.textContent = message;
    show(errorEl);
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function renderPost(post) {
    const pv = post.platform_variations || {};
    const creative = [
      post.suggested_creative_type && `Type: ${post.suggested_creative_type}`,
      post.text_overlay_suggestion && `Overlay: ${post.text_overlay_suggestion}`,
      post.color_theme_suggestion && `Theme: ${post.color_theme_suggestion}`,
    ].filter(Boolean);

    const hashtagsHtml = (post.hashtags || []).length
      ? (post.hashtags || [])
          .map(function (h) {
            const tag = h.startsWith("#") ? h : "#" + h;
            return '<span class="hashtag">' + escapeHtml(tag) + "</span>";
          })
          .join("")
      : "<span class=\"value\">—</span>";

    return (
      '<article class="post-card">' +
      '<div class="post-header">' +
      '<span class="post-number">Post ' + escapeHtml(String(post.post_number)) + "</span>" +
      '<span class="post-topic">' + escapeHtml(post.post_topic || "Untitled") + "</span>" +
      "</div>" +
      '<div class="post-block">' +
      '<div class="label">Caption</div>' +
      '<div class="value">' + escapeHtml(post.caption || "—") + "</div>" +
      "</div>" +
      '<div class="post-block platforms">' +
      '<div class="label">Platform variations</div>' +
      '<div class="value">' +
      '<div class="platform-item"><strong>Instagram</strong>' + escapeHtml(pv.instagram || "—") + "</div>" +
      '<div class="platform-item"><strong>LinkedIn</strong>' + escapeHtml(pv.linkedin || "—") + "</div>" +
      '<div class="platform-item"><strong>Facebook</strong>' + escapeHtml(pv.facebook || "—") + "</div>" +
      "</div>" +
      "</div>" +
      '<div class="post-block">' +
      '<div class="label">Hashtags</div>' +
      '<div class="hashtags-list">' + hashtagsHtml + "</div>" +
      "</div>" +
      '<div class="post-block">' +
      '<div class="label">CTA</div>' +
      '<div class="value">' + escapeHtml(post.cta || "—") + "</div>" +
      "</div>" +
      '<div class="post-block">' +
      '<div class="label">Creative suggestion</div>' +
      '<div class="creative-suggestion value">' +
      (creative.length ? creative.map(function (c) { return "<span>" + escapeHtml(c) + "</span>"; }).join("") : "<span>—</span>") +
      "</div>" +
      "</div>" +
      '<div class="post-block">' +
      '<div class="label">Image prompt</div>' +
      '<div class="image-prompt-box">' + escapeHtml(post.ai_image_prompt || "—") + "</div>" +
      "</div>" +
      "</article>"
    );
  }

  function displayResults(data) {
    resultsBusiness.textContent = data.business_name || "Your business";
    postsContainer.innerHTML = (data.generated_posts || []).map(renderPost).join("");
    show(results);
    results.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var num = parseInt(document.getElementById("number_of_posts").value, 10) || 3;
    num = Math.min(30, Math.max(1, num));

    var payload = {
      business_name: document.getElementById("business_name").value.trim(),
      industry: document.getElementById("industry").value.trim(),
      target_audience: document.getElementById("target_audience").value.trim(),
      location: document.getElementById("location").value.trim(),
      business_goal: document.getElementById("business_goal").value,
      tone: document.getElementById("tone").value,
      number_of_posts: num,
    };

    setLoading(true);

    fetch(API_BASE + "/api/v1/content/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then(function (res) {
        if (!res.ok) {
          return res.json().then(
            function (body) {
              throw new Error(body.detail || res.statusText || "Request failed");
            },
            function () {
              throw new Error(res.statusText || "Request failed");
            }
          );
        }
        return res.json();
      })
      .then(function (data) {
        setLoading(false);
        displayResults(data);
      })
      .catch(function (err) {
        var message = err.message || "Something went wrong. Is the backend running at " + API_BASE + "?";
        showError(message);
      });
  });
})();
