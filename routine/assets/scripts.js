/** Initialise dash_clientside to allow inline clientside callback */
if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    base: {
        getTimezone: () => {
            return Intl.DateTimeFormat().resolvedOptions().timeZone
        },
        switchScheme: (isLightMode) => {
            return isLightMode ? 'light' : 'dark'
        },
    }
});
