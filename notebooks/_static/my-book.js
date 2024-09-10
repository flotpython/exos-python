// standard JS additions for our jupyter books

// expose to the console
const cheatCorrige = () => {
    // open a corrige file which is located under
    // the .teacher folder with an extra "corrige-" suffix
    // e.g. "my-book-nb.html" -> ".teacher/my-book-nb-corrige.html"
    const currentLocation = window.location.href
    let newLocation
    if (currentLocation.includes("-corrige"))
        // undo: go back to the student version
        newLocation = currentLocation.replace(
            /(.*)\/\.teacher\/([A-Za-z0-9_-]+)-corrige-nb\.html/gm,
            "$1/$2-nb.html"
        )
    else
        newLocation = currentLocation.replace(
            /(.*)\/([A-Za-z0-9_-]+)-nb\.html/gm,
            "$1/.teacher/$2-corrige-nb.html"
        )
    if (newLocation === currentLocation) {
        console.log("from my-book.js: no corrige file found")
        return
    }
    window.location.href = newLocation
}

// run the following code when the page is loaded
window.addEventListener('load',
    () => {

        const urlTocEntriesOpenInNewTab = () => {
            console.log("from my-book.js: url-typed toc entries open in a separate tab")
            document.querySelectorAll("nav a.reference.external")
                .forEach(node => node.target = "_blank")
        }

        // define a keyboard shortcut to open the corrige file
        // want to be able to communicate the use of Ctrl-Shift-?
        // very surprisingly, it is incredibly hard to catch a keyboard shortcut
        // properly i.e. regardless of the keyboard layout
        // given that keypress is deprecated, we are left with keydown
        // as beforeinput does not even trigger in our case (not changing the dom)
        // it turns out that neither the key nor code properties are reliable
        // across qwerty / azerty / layouts - I haven't tried dvorak
        // so here's the trade off that I came up with:
        // the 'key' property seems to always refer to the lowercase character
        // on a  qwerty I have / being the lowercase and ? the uppercase
        // on an azerty I have , being the lowercase and ? the uppercase
        // on a qwerty linux,  ? is the lowercase and / the uppercase
        const lowercases = { '/': true, ',': true, '?': true }
        const cheatCorrigeShortcut = () => {
            console.log("from my-book.js: define corrige magic shortcut")
            document.addEventListener("keydown", (event) => {
                // console.log("keydown", event)
                if (event.key in lowercases && event.ctrlKey && event.shiftKey) {
                    cheatCorrige()
                }
            })
        }

        // inject class corrige when relevant
        const outlineCorrige = () => {
            if (window.location.href.includes("corrige")) {
                document.body.classList.add("corrige")
            }
        }

        // our setup
        urlTocEntriesOpenInNewTab()
        outlineCorrige()
        cheatCorrigeShortcut()
    })
