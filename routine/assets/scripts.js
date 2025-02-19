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
        switchRememberMe: (remember) => {
            if (!remember) return [false, 1]
            return ["local", 1]
        },
        highlightLink: (pathname, ids, icons) => {
            const pattern = new RegExp(`${pathname}(/|$)`)
            const classNames = []
            const newIcons = []
            ids.forEach((id, i) => {
                if (id.href.match(pattern)) {
                    classNames.push("footer-link active")
                    newIcons.push(icons[i].replace(/regular$/, "filled"))
                } else {
                    classNames.push("footer-link")
                    newIcons.push(icons[i].replace(/filled$/, "regular"))
                }
            })
            return [classNames, newIcons]
        },
        changePastDate: (clicks, ids) => {
            if (!clicks.some(x => !!x)) return [dash_clientside.no_update, dash_clientside.no_update]
            const value = dash_clientside.callback_context.triggered_id.date
            return [
                value,
                ids.map(id => id.date == value ? "date-btn active" : "date-btn")
            ]
        },
        scrollToLatest: (id) => {
            const element = document.getElementById(id).children[0]
            element.scrollBy(element.scrollWidth, 0)
            return dash_clientside.no_update
        },
        showConnecting: (connected) => connected ? "main-loader" : "main-loader visible",
    }
});
