(function () {
    const root = document.documentElement;
    const storageKey = 'promiselane-theme';
    let savedTheme = null;

    try {
        savedTheme = window.localStorage.getItem(storageKey);
    } catch (error) {
        console.error('Unable to read the saved theme preference.', error);
    }

    if (savedTheme === 'dark' || savedTheme === 'light') {
        root.dataset.theme = savedTheme;
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        root.dataset.theme = 'dark';
    }

    document.addEventListener('DOMContentLoaded', function () {
        const toggle = document.querySelector('[data-theme-toggle]');
        if (!toggle) {
            return;
        }

        const icon = toggle.querySelector('[data-theme-icon]');
        const label = toggle.querySelector('[data-theme-label]');

        function updateToggle() {
            const isDark = root.dataset.theme === 'dark';
            toggle.setAttribute('aria-pressed', String(isDark));
            toggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
            icon.textContent = isDark ? '☀' : '☾';
            label.textContent = isDark ? 'Light mode' : 'Dark mode';
        }

        toggle.addEventListener('click', function () {
            const nextTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
            root.dataset.theme = nextTheme;
            updateToggle();

            try {
                window.localStorage.setItem(storageKey, nextTheme);
            } catch (error) {
                console.error('Unable to save the theme preference.', error);
            }
        });

        updateToggle();
    }, { once: true });
}());
