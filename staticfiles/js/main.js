document.addEventListener("DOMContentLoaded", function () {
    // ═══════ ELEMENT REFERENCES ═══════
    const inputTitle = document.getElementById('input-title');
    const inputProfessionalTitle = document.getElementById('input-professional-title');
    const inputTagline = document.getElementById('input-tagline');
    const inputBio = document.getElementById('input-bio');
    const inputSkills = document.getElementById('input-skills');
    const inputTemplate = document.getElementById('input-template');
    const inputAccentColor = document.getElementById('input-accent-color');
    const inputProfileImage = document.getElementById('input-profile-image');

    const btnSaveDraft = document.getElementById('btn-save-draft');
    const portfolioForm = document.getElementById('portfolio-form');
    const filePreviewImg = document.getElementById('file-preview-img');
    const previewIframe = document.getElementById('preview-iframe');
    const browserWindow = document.getElementById('browser-window');

    // ═══════ DEVICE SWITCHER (DESKTOP, TABLET, MOBILE) ═══════
    const deviceBtns = document.querySelectorAll('.device-btn');
    deviceBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            deviceBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const device = this.getAttribute('data-device');
            if (browserWindow) {
                browserWindow.className = 'browser-window device-' + device;
            }
        });
    });

    // ═══════ TABS NAVIGATION ═══════
    const tabs = document.querySelectorAll('.tab');
    const sections = document.querySelectorAll('.form-section');
    const activeTabInput = document.getElementById('active_tab');

    window.activateTab = function (targetId) {
        tabs.forEach(t => t.classList.remove('active'));
        sections.forEach(s => s.style.display = 'none');
        const targetTab = document.querySelector('.tab[data-target="' + targetId + '"]');
        const targetSection = document.getElementById(targetId);
        if (targetTab) targetTab.classList.add('active');
        if (targetSection) targetSection.style.display = 'block';

        if (activeTabInput) {
            const map = {
                'section-content': 'content',
                'section-projects': 'projects',
                'section-design': 'design',
                'section-export': 'export'
            };
            activeTabInput.value = map[targetId] || 'content';
        }
    };

    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            activateTab(this.getAttribute('data-target'));
        });
    });

    // Auto-open tab from URL ?tab=...
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    if (tabParam) {
        const tabMap = {
            'projects': 'section-projects',
            'content': 'section-content',
            'design': 'section-design',
            'export': 'section-export',
            'settings': 'section-export'
        };
        const sectionId = tabMap[tabParam];
        if (sectionId) {
            activateTab(sectionId);
            window.history.replaceState({}, '', window.location.pathname);
        }
    }

    // ═══════ TEMPLATE SELECTION ═══════
    const templateCards = document.querySelectorAll('.template-card');

    function applyTemplatePreview(templateName) {
        if (inputTemplate) inputTemplate.value = templateName;
        if (previewIframe && previewIframe.src) {
            const url = new URL(previewIframe.src, window.location.origin);
            url.searchParams.set('preview_template', templateName);
            previewIframe.src = url.pathname + url.search;
        }
    }

    window.refreshPreviewIframe = function () {
        if (previewIframe && previewIframe.src) {
            const currentSrc = previewIframe.src;
            previewIframe.src = '';
            setTimeout(() => { previewIframe.src = currentSrc; }, 50);
            if (window.showToast) window.showToast('Live preview refreshed', 'info');
        }
    };

    templateCards.forEach(card => {
        card.addEventListener('click', function () {
            templateCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            const selectedTemplate = this.getAttribute('data-template');
            applyTemplatePreview(selectedTemplate);
        });
    });

    // ═══════ ACCENT COLOR PRESETS ═══════
    window.setAccentColor = function (colorHex) {
        if (inputAccentColor) inputAccentColor.value = colorHex;
        window.showToast('Accent color updated to ' + colorHex, 'success');
    };

    // ═══════ PROFILE IMAGE PREVIEW ═══════
    if (inputProfileImage) {
        inputProfileImage.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    if (filePreviewImg) filePreviewImg.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ═══════ DROPDOWN ═══════
    const dropdown = document.getElementById('view-live-dropdown');
    const btnViewLive = document.getElementById('btn-view-live');
    if (btnViewLive && dropdown) {
        btnViewLive.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdown.classList.toggle('open');
        });
        document.addEventListener('click', function (e) {
            if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
        });
    }

    // ═══════ SAVE BUTTON ═══════
    if (btnSaveDraft && portfolioForm) {
        btnSaveDraft.addEventListener('click', function () {
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
            this.disabled = true;
            portfolioForm.submit();
        });
    }

    // ═══════ TOAST NOTIFICATIONS ═══════
    window.showToast = function (message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-info'}"></i><span>${message}</span><button class="toast-close" onclick="this.parentElement.remove()">&times;</button>`;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    };

    // ═══════ RESUME UPLOAD & PARSING ═══════
    const resumeFileInput = document.getElementById('resume-file-input');
    const resumeDropzone = document.getElementById('resume-dropzone');
    const btnResumeModalOpen = document.getElementById('btn-resume-modal-open');

    if (btnResumeModalOpen) {
        btnResumeModalOpen.addEventListener('click', function () {
            activateTab('section-ai');
            if (resumeDropzone) resumeDropzone.scrollIntoView({ behavior: 'smooth' });
        });
    }

    function uploadResumeFile(file) {
        if (!file || !file.name.endsWith('.pdf')) {
            showToast('Please select a valid PDF file.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('resume_pdf', file);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        showToast('Uploading & parsing PDF resume...', 'info');

        fetch('/api/import-resume/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    showToast('Resume imported! Reloading fields...', 'success');
                    setTimeout(() => window.location.reload(), 1200);
                } else {
                    showToast(data.message || 'Failed to parse resume.', 'error');
                }
            })
            .catch(err => {
                showToast('Error uploading resume: ' + err.message, 'error');
            });
    }

    if (resumeFileInput) {
        resumeFileInput.addEventListener('change', function () {
            if (this.files.length > 0) uploadResumeFile(this.files[0]);
        });
    }

    if (resumeDropzone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            resumeDropzone.addEventListener(eventName, e => { e.preventDefault(); resumeDropzone.classList.add('dragover'); });
        });
        ['dragleave', 'drop'].forEach(eventName => {
            resumeDropzone.addEventListener(eventName, e => { e.preventDefault(); resumeDropzone.classList.remove('dragover'); });
        });
        resumeDropzone.addEventListener('drop', e => {
            const dt = e.dataTransfer;
            if (dt.files.length > 0) uploadResumeFile(dt.files[0]);
        });
    }

    // ═══════ AI CONTENT GENERATOR ═══════
    const btnGenerateAiTool = document.getElementById('btn-generate-ai-tool');
    const aiToolType = document.getElementById('ai-tool-type');
    const aiToolPrompt = document.getElementById('ai-tool-prompt');
    const aiResultBox = document.getElementById('ai-result-box');
    const aiResultText = document.getElementById('ai-result-text');

    if (btnGenerateAiTool) {
        btnGenerateAiTool.addEventListener('click', function () {
            const prompt = aiToolPrompt.value.trim();
            const type = aiToolType.value;
            if (!prompt) {
                showToast('Please enter a prompt for AI.', 'error');
                return;
            }

            btnGenerateAiTool.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';
            btnGenerateAiTool.disabled = true;

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch('/api/generate-ai-content/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ prompt: prompt, type: type })
            })
                .then(res => res.json())
                .then(data => {
                    btnGenerateAiTool.innerHTML = '<i class="fa-solid fa-sparkles"></i> Generate AI Content';
                    btnGenerateAiTool.disabled = false;
                    if (data.status === 'success') {
                        if (aiResultText) aiResultText.value = data.result;
                        if (aiResultBox) aiResultBox.style.display = 'block';
                        showToast('AI content generated!', 'success');
                    } else {
                        showToast(data.message || 'Generation failed.', 'error');
                    }
                })
                .catch(err => {
                    btnGenerateAiTool.innerHTML = '<i class="fa-solid fa-sparkles"></i> Generate AI Content';
                    btnGenerateAiTool.disabled = false;
                    showToast('AI Generation error: ' + err.message, 'error');
                });
        });
    }

    window.copyAiResult = function () {
        if (aiResultText) {
            navigator.clipboard.writeText(aiResultText.value);
            showToast('Result copied to clipboard!', 'success');
        }
    };

    // AI Inline Helper
    window.openAiGeneratorFor = function (type, fieldId) {
        const field = document.getElementById(fieldId);
        const currentVal = field ? field.value : '';
        const prompt = prompt || currentVal || 'Software Developer';

        showToast('Generating AI suggestion...', 'info');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/api/generate-ai-content/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ prompt: prompt, type: type })
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success' && field) {
                    field.value = data.result;
                    showToast('Field updated with AI text!', 'success');
                }
            });
    };

    // AI Modal Shortcut
    const btnAiModalOpen = document.getElementById('btn-ai-modal-open');
    const aiModalOverlay = document.getElementById('ai-modal-overlay');
    const btnModalAiSubmit = document.getElementById('btn-modal-ai-submit');
    const modalAiPrompt = document.getElementById('modal-ai-prompt');
    const modalAiType = document.getElementById('modal-ai-type');
    const modalAiResultWrap = document.getElementById('modal-ai-result-wrap');
    const modalAiResult = document.getElementById('modal-ai-result');

    if (btnAiModalOpen && aiModalOverlay) {
        btnAiModalOpen.addEventListener('click', () => { aiModalOverlay.classList.add('open'); });
    }
    window.closeAiModal = function () {
        if (aiModalOverlay) aiModalOverlay.classList.remove('open');
    };

    if (btnModalAiSubmit) {
        btnModalAiSubmit.addEventListener('click', function () {
            const prompt = modalAiPrompt.value.trim();
            const type = modalAiType.value;
            if (!prompt) return showToast('Prompt is required.', 'error');

            btnModalAiSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';
            btnModalAiSubmit.disabled = true;

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch('/api/generate-ai-content/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ prompt: prompt, type: type })
            })
                .then(res => res.json())
                .then(data => {
                    btnModalAiSubmit.innerHTML = '<i class="fa-solid fa-sparkles"></i> Generate Text';
                    btnModalAiSubmit.disabled = false;
                    if (data.status === 'success') {
                        modalAiResult.value = data.result;
                        modalAiResultWrap.style.display = 'block';
                    }
                });
        });
    }

    // ═══════ GITHUB REPO AUTO-IMPORT ═══════
    window.importGithubProjects = function () {
        const username = prompt('Enter your GitHub Username (or leave blank to use saved link):');
        showToast('Fetching repositories from GitHub...', 'info');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/api/import-github-repos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ username: username || '' })
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    showToast(data.message, 'success');
                    setTimeout(() => window.location.reload(), 1200);
                } else {
                    showToast(data.message || 'GitHub import failed.', 'error');
                }
            })
            .catch(err => showToast('GitHub API Error: ' + err.message, 'error'));
    };

    // ═══════ SUB-FORM SUBMISSIONS (EDUCATION, EXPERIENCE, CERTIFICATES) ═══════
    window.submitEducation = function () {
        const degree = document.getElementById('edu-degree').value.trim();
        const college = document.getElementById('edu-college').value.trim();
        const year = document.getElementById('edu-year').value.trim();
        const cgpa = document.getElementById('edu-cgpa').value.trim();

        if (!degree || !college) return showToast('Degree and College are required.', 'error');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('degree', degree);
        formData.append('college', college);
        formData.append('year', year);
        formData.append('cgpa', cgpa);

        fetch('/add-education/', { method: 'POST', headers: { 'X-CSRFToken': csrfToken }, body: formData })
            .then(() => window.location.reload());
    };

    window.submitExperience = function () {
        const company = document.getElementById('exp-company').value.trim();
        const role = document.getElementById('exp-role').value.trim();
        const duration = document.getElementById('exp-duration').value.trim();
        const description = document.getElementById('exp-description').value.trim();

        if (!company || !role) return showToast('Company and Role are required.', 'error');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('company', company);
        formData.append('role', role);
        formData.append('duration', duration);
        formData.append('description', description);

        fetch('/add-experience/', { method: 'POST', headers: { 'X-CSRFToken': csrfToken }, body: formData })
            .then(() => window.location.reload());
    };

    window.submitCertificate = function () {
        const name = document.getElementById('cert-name').value.trim();
        const organization = document.getElementById('cert-org').value.trim();
        const year = document.getElementById('cert-year').value.trim();
        const link = document.getElementById('cert-link').value.trim();

        if (!name || !organization) return showToast('Certificate name and organization are required.', 'error');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('name', name);
        formData.append('organization', organization);
        formData.append('year', year);
        formData.append('link', link);

        fetch('/add-certificate/', { method: 'POST', headers: { 'X-CSRFToken': csrfToken }, body: formData })
            .then(() => window.location.reload());
    };

    // ═══════ DELETE MODAL ═══════
    window._deleteProjectId = null;
    window.confirmDeleteProject = function (projectId, projectTitle) {
        window._deleteProjectId = projectId;
        const modal = document.getElementById('delete-modal-overlay');
        const desc = document.getElementById('modal-project-name');
        if (desc) desc.textContent = 'Are you sure you want to delete "' + projectTitle + '"?';
        if (modal) modal.classList.add('open');
    };

    window.closeDeleteModal = function () {
        const modal = document.getElementById('delete-modal-overlay');
        if (modal) modal.classList.remove('open');
        window._deleteProjectId = null;
    };

    const confirmDeleteBtn = document.getElementById('btn-confirm-delete');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function () {
            if (window._deleteProjectId) {
                const deleteForm = document.getElementById('delete-form-' + window._deleteProjectId);
                if (deleteForm) deleteForm.submit();
            }
        });
    }

    // ═══════ PROJECT EDITING ═══════
    window.editProject = function (id, title, desc, githubLink, demoLink, tags, editUrl) {
        activateTab('section-projects');

        const form = document.getElementById('project-form');
        if (form) form.action = editUrl;

        const formTitle = document.getElementById('project-form-title');
        if (formTitle) formTitle.textContent = 'Edit Project';

        document.getElementById('project-title').value = title;
        document.getElementById('project-desc').value = desc;
        if (document.getElementById('project-github-link')) document.getElementById('project-github-link').value = githubLink;
        if (document.getElementById('project-demo-link')) document.getElementById('project-demo-link').value = demoLink;
        document.getElementById('project-tags').value = tags;

        const btnSubmit = document.getElementById('btn-submit-project');
        if (btnSubmit) btnSubmit.innerHTML = '<i class="fa-solid fa-pen"></i> Update Project';

        const btnCancel = document.getElementById('btn-cancel-edit');
        if (btnCancel) btnCancel.style.display = 'block';
    };

    window.cancelEditProject = function () {
        const form = document.getElementById('project-form');
        if (form) {
            form.reset();
            form.action = '/add-project/';
        }
        const formTitle = document.getElementById('project-form-title');
        if (formTitle) formTitle.textContent = 'Add New Project';

        const btnSubmit = document.getElementById('btn-submit-project');
        if (btnSubmit) btnSubmit.innerHTML = '<i class="fa-solid fa-plus"></i> Add Project';

        const btnCancel = document.getElementById('btn-cancel-edit');
        if (btnCancel) btnCancel.style.display = 'none';
    };
});
