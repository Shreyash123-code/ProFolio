document.addEventListener("DOMContentLoaded", function() {
    // ═══════ ELEMENT REFERENCES ═══════
    const inputTitle = document.getElementById('input-title');
    const inputTagline = document.getElementById('input-tagline');
    const inputBio = document.getElementById('input-bio');
    const inputSkills = document.getElementById('input-skills');
    const inputEmail = document.getElementById('input-email');
    const inputGithub = document.getElementById('input-github');
    const inputLinkedin = document.getElementById('input-linkedin');
    const inputTheme = document.getElementById('input-theme');
    const inputTemplate = document.getElementById('input-template');
    const inputProfileImage = document.getElementById('input-profile-image');
    
    const previewTitle = document.getElementById('preview-title');
    const previewTagline = document.getElementById('preview-tagline');
    const previewBio = document.getElementById('preview-bio');
    const previewImage = document.getElementById('preview-image');
    const previewGithub = document.getElementById('preview-github');
    const previewLinkedin = document.getElementById('preview-linkedin');
    const previewEmailIcon = document.getElementById('preview-email-icon');
    const previewSkills = document.getElementById('preview-skills');
    const previewSkillsList = document.getElementById('preview-skills-list');
    
    const btnSaveDraft = document.getElementById('btn-save-draft');
    const portfolioForm = document.getElementById('portfolio-form');
    const filePreviewImg = document.getElementById('file-preview-img');

    // ═══════ LIVE TEXT PREVIEW ═══════
    function setupLivePreview(input, preview, defaultText, property = 'textContent') {
        if (!input || !preview) return;
        input.addEventListener('input', () => {
            const val = input.value.trim();
            if (property === 'textContent') {
                preview.textContent = val || defaultText;
            } else if (property === 'href') {
                preview.href = val || '#';
            }
        });
    }
    
    setupLivePreview(inputTitle, previewTitle, 'Your Name & Title');
    setupLivePreview(inputTagline, previewTagline, 'Your tagline goes here');
    setupLivePreview(inputBio, previewBio, 'Write a short introduction about yourself.');
    setupLivePreview(inputGithub, previewGithub, '#', 'href');
    setupLivePreview(inputLinkedin, previewLinkedin, '#', 'href');

    // Skills live preview
    if (inputSkills && previewSkills && previewSkillsList) {
        inputSkills.addEventListener('input', () => {
            const val = inputSkills.value.trim();
            if (val) {
                previewSkills.style.display = 'block';
                const skills = val.split(',').map(s => s.trim()).filter(s => s);
                previewSkillsList.innerHTML = skills.map(s => 
                    `<span class="preview-skill-tag">${s}</span>`
                ).join('');
            } else {
                previewSkills.style.display = 'none';
                previewSkillsList.innerHTML = '';
            }
        });
    }

    // Email live preview
    if (inputEmail && previewEmailIcon) {
        inputEmail.addEventListener('input', () => {
            const val = inputEmail.value.trim();
            previewEmailIcon.style.display = val ? 'inline' : 'none';
        });
    }

    // ═══════ IMAGE PREVIEW ═══════
    if (inputProfileImage) {
        inputProfileImage.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (previewImage) previewImage.src = e.target.result;
                    if (filePreviewImg) filePreviewImg.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ═══════ TABS ═══════
    const tabs = document.querySelectorAll('.tab');
    const sections = document.querySelectorAll('.form-section');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Deactivate all
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.style.display = 'none');
            
            // Activate clicked
            this.classList.add('active');
            const target = this.getAttribute('data-target');
            const targetSection = document.getElementById(target);
            if (targetSection) {
                targetSection.style.display = 'block';
            }
        });
    });

    // ═══════ TEMPLATE SELECTION ═══════
    const templateCards = document.querySelectorAll('.template-card');
    const browserWindow = document.getElementById('browser-window');

    function applyTemplatePreview(templateName) {
        if (browserWindow) {
            browserWindow.setAttribute('data-template', templateName);
        }
    }

    templateCards.forEach(card => {
        card.addEventListener('click', function() {
            templateCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');

            const selectedTemplate = this.getAttribute('data-template');
            if (inputTemplate) inputTemplate.value = selectedTemplate;
            applyTemplatePreview(selectedTemplate);
        });
    });

    // Apply current saved template on page load
    if (inputTemplate && inputTemplate.value) {
        applyTemplatePreview(inputTemplate.value);
    }

    // ═══════ DROPDOWN ═══════
    const dropdown = document.getElementById('view-live-dropdown');
    const btnViewLive = document.getElementById('btn-view-live');
    
    if (btnViewLive && dropdown) {
        btnViewLive.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('open');
        });
        
        // Close on outside click
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('open');
            }
        });
    }

    // ═══════ SAVE ═══════
    if (btnSaveDraft && portfolioForm) {
        btnSaveDraft.addEventListener('click', function() {
            // Show saving indicator
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
            this.disabled = true;
            portfolioForm.submit();
        });
    }

    // ═══════ AUTO-DISMISS TOASTS ═══════
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    });
});
