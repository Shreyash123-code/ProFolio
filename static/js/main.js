document.addEventListener("DOMContentLoaded", function() {
    // ═══════ ELEMENT REFERENCES ═══════
    const inputTitle = document.getElementById('input-title');
    const inputTagline = document.getElementById('input-tagline');
    const inputBio = document.getElementById('input-bio');
    const inputSkills = document.getElementById('input-skills');
    const inputEmail = document.getElementById('input-email');
    const inputGithub = document.getElementById('input-github');
    const inputLinkedin = document.getElementById('input-linkedin');
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
    function setupLivePreview(input, preview, defaultText, property) {
        property = property || 'textContent';
        if (!input || !preview) return;
        input.addEventListener('input', function() {
            var val = input.value.trim();
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
        inputSkills.addEventListener('input', function() {
            var val = inputSkills.value.trim();
            if (val) {
                previewSkills.style.display = 'block';
                var skills = val.split(',').map(function(s) { return s.trim(); }).filter(function(s) { return s; });
                previewSkillsList.innerHTML = skills.map(function(s) {
                    return '<span class="preview-skill-tag">' + s + '</span>';
                }).join('');
            } else {
                previewSkills.style.display = 'none';
                previewSkillsList.innerHTML = '';
            }
        });
    }

    // Email icon live preview
    if (inputEmail && previewEmailIcon) {
        inputEmail.addEventListener('input', function() {
            previewEmailIcon.style.display = inputEmail.value.trim() ? 'inline' : 'none';
        });
    }

    // ═══════ IMAGE PREVIEW ═══════
    if (inputProfileImage) {
        inputProfileImage.addEventListener('change', function() {
            var file = this.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    if (previewImage) previewImage.src = e.target.result;
                    if (filePreviewImg) filePreviewImg.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ═══════ TABS ═══════
    var tabs = document.querySelectorAll('.tab');
    var sections = document.querySelectorAll('.form-section');

    function activateTab(targetId) {
        tabs.forEach(function(t) { t.classList.remove('active'); });
        sections.forEach(function(s) { s.style.display = 'none'; });
        var targetTab = document.querySelector('.tab[data-target="' + targetId + '"]');
        var targetSection = document.getElementById(targetId);
        if (targetTab) targetTab.classList.add('active');
        if (targetSection) targetSection.style.display = 'block';
    }

    tabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            activateTab(this.getAttribute('data-target'));
        });
    });

    // Auto-open tab from URL ?tab=projects (after project save/delete/edit)
    var urlParams = new URLSearchParams(window.location.search);
    var tabParam = urlParams.get('tab');
    if (tabParam) {
        var tabMap = {
            'projects': 'section-projects',
            'content': 'section-content',
            'design': 'section-design',
            'settings': 'section-settings'
        };
        var sectionId = tabMap[tabParam];
        if (sectionId) {
            activateTab(sectionId);
            // Clean URL without reloading
            window.history.replaceState({}, '', window.location.pathname);
        }
    }

    // ═══════ TEMPLATE SELECTION ═══════
    var templateCards = document.querySelectorAll('.template-card');
    var browserWindow = document.getElementById('browser-window');

    function applyTemplatePreview(templateName) {
        if (browserWindow) {
            browserWindow.setAttribute('data-template', templateName);
        }
        
        // Update View Website links dynamically
        var viewLinks = document.querySelectorAll('a.dropdown-item[href^="/p/"], a.export-card[href^="/p/"]');
        viewLinks.forEach(function(link) {
            var url = new URL(link.href, window.location.origin);
            url.searchParams.set('preview_template', templateName);
            link.href = url.pathname + url.search;
        });
    }

    templateCards.forEach(function(card) {
        card.addEventListener('click', function() {
            templateCards.forEach(function(c) { c.classList.remove('selected'); });
            this.classList.add('selected');
            var selectedTemplate = this.getAttribute('data-template');
            if (inputTemplate) inputTemplate.value = selectedTemplate;
            applyTemplatePreview(selectedTemplate);
        });
    });

    if (inputTemplate && inputTemplate.value) {
        applyTemplatePreview(inputTemplate.value);
    }

    // ═══════ DROPDOWN ═══════
    var dropdown = document.getElementById('view-live-dropdown');
    var btnViewLive = document.getElementById('btn-view-live');

    if (btnViewLive && dropdown) {
        btnViewLive.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('open');
        });
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('open');
            }
        });
    }

    // ═══════ SAVE BUTTON ═══════
    if (btnSaveDraft && portfolioForm) {
        btnSaveDraft.addEventListener('click', function() {
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
            this.disabled = true;
            portfolioForm.submit();
        });
    }

    // ═══════ AUTO-DISMISS TOASTS ═══════
    var toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toast) {
        setTimeout(function() {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(function() { toast.remove(); }, 300);
        }, 4000);
    });

    // ═══════ DELETE MODAL CONFIRM BUTTON ═══════
    var confirmDeleteBtn = document.getElementById('btn-confirm-delete');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function() {
            if (window._deleteProjectId) {
                var deleteForm = document.getElementById('delete-form-' + window._deleteProjectId);
                if (deleteForm) {
                    confirmDeleteBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Deleting...';
                    confirmDeleteBtn.disabled = true;
                    deleteForm.submit();
                }
            }
        });
    }

    // Close modal when clicking the overlay background
    var modalOverlay = document.getElementById('delete-modal-overlay');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                window.closeDeleteModal();
            }
        });
    }
});

// ═══════ PROJECT EDITING ═══════
window.editProject = function(id, title, desc, link, tags, editUrl) {
    // Switch to projects tab
    var projectTabBtn = document.querySelector('.tab[data-target="section-projects"]');
    if (projectTabBtn && !projectTabBtn.classList.contains('active')) {
        projectTabBtn.click();
    }

    // Update form action to the edit URL
    var form = document.getElementById('project-form');
    if (form) form.action = editUrl;

    // Update section header
    var formTitle = document.getElementById('project-form-title');
    if (formTitle) formTitle.textContent = 'Edit Project';

    // Fill the form fields
    var titleField = document.getElementById('project-title');
    if (titleField) titleField.value = title;

    var descField = document.getElementById('project-desc');
    if (descField) descField.value = desc;

    var linkField = document.getElementById('project-link');
    if (linkField) linkField.value = link;

    var tagsField = document.getElementById('project-tags');
    if (tagsField) tagsField.value = tags;

    // Update submit button
    var btnSubmit = document.getElementById('btn-submit-project');
    if (btnSubmit) {
        btnSubmit.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Update Project';
        btnSubmit.style.background = 'linear-gradient(135deg, #059669, #047857)';
        btnSubmit.style.boxShadow = '0 2px 8px rgba(5,150,105,0.3)';
    }

    // Show cancel button
    var btnCancel = document.getElementById('btn-cancel-edit');
    if (btnCancel) btnCancel.style.display = 'flex';

    // Scroll to form
    if (form) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

window.cancelEditProject = function() {
    var form = document.getElementById('project-form');
    if (form) {
        form.reset();
        // Reset action to the add endpoint
        form.action = '/add-project/';
    }

    var formTitle = document.getElementById('project-form-title');
    if (formTitle) formTitle.textContent = 'Add New Project';

    var btnSubmit = document.getElementById('btn-submit-project');
    if (btnSubmit) {
        btnSubmit.innerHTML = '<i class="fa-solid fa-plus"></i> Add Project';
        btnSubmit.style.background = '';
        btnSubmit.style.boxShadow = '';
    }

    var btnCancel = document.getElementById('btn-cancel-edit');
    if (btnCancel) btnCancel.style.display = 'none';
};

// ═══════ DELETE MODAL ═══════
window._deleteProjectId = null;

window.confirmDeleteProject = function(projectId, projectTitle) {
    window._deleteProjectId = projectId;
    var modal = document.getElementById('delete-modal-overlay');
    var desc = document.getElementById('modal-project-name');
    if (desc) {
        desc.textContent = 'Are you sure you want to delete "' + projectTitle + '"? This action cannot be undone.';
    }
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    }
};

window.closeDeleteModal = function() {
    var modal = document.getElementById('delete-modal-overlay');
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }
    window._deleteProjectId = null;
};
