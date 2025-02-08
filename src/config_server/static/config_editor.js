AutoComplete = () => {
    const exchangeAutoComplete = new autoComplete({ 
        placeHolder: "Search for exchange",
        selector: '#exchange',
        data:{
            src: async (query) => {
                try {
                    const exchangeInput = document.getElementById("exchange");
                    exchangeInput.setAttribute("placeholder", "Loading...");
                    const source = await fetch(exchangeInput.dataset.autocomplete + '?q=' + query);
                    const fetchedData = await source.json();
                    exchangeInput.setAttribute("placeholder", exchangeAutoComplete.placeHolder);
                    return fetchedData;
                } catch (error) {
                    return error;
                }
              },
        },
        resultsList: {
            element: (list, data) => {
                if (!data.results.length) {
                    const message = document.createElement("div");
                    message.setAttribute("class", "no_result");
                    message.innerHTML = `Found No Results for "${data.query}"`;
                    list.prepend(message);
                }
            },
            noResults: true,
        },
        resultItem: {
            highlight: {
                render: true
            }
        },
        events: {
            input: {
                selection: (event) => {
                    const instrumentInput = document.getElementById("instrument");
                    const selection = event.detail.selection.value;
                    exchangeAutoComplete.input.value = selection;
                    instrumentInput.value = null;
                }
            }
        }
      });
      const instrumentAutoComplete = new autoComplete({ 
        placeHolder: "Search for instrument",
        selector: '#instrument',
        data:{
            src: async (query) => {
                try {
                    const instrumentInput = document.getElementById("instrument");
                    const exchangeInput = document.getElementById("exchange");
                    instrumentInput.setAttribute("placeholder", "Loading...");
                    // Fetch External Data Source
                    const source = await fetch(instrumentInput.dataset.autocomplete + "/" + exchangeInput.value + '/markets?q=' + query);
                    const data = await source.json();
                    // Post Loading placeholder text
                    instrumentInput.setAttribute("placeholder", instrumentAutoComplete.placeHolder);
                    // Returns Fetched data
                    return data;
                } catch (error) {
                    return error;
                }
              },
        },
        resultsList: {
            element: (list, data) => {
                if (!data.results.length) {
                    // Create "No Results" message element
                    const message = document.createElement("div");
                    // Add class to the created element
                    message.setAttribute("class", "no_result");
                    // Add message text content
                    message.innerHTML = `Found No Results for "${data.query}"`;
                    // Append message element to the results list
                    list.prepend(message);
                }
            },
            noResults: true,
        },
        resultItem: {
            highlight: {
                render: true
            }
        },
        events: {
            input: {
                selection: (event) => {
                    const instrumentInput = document.getElementById("instrument");
                    const selection = event.detail.selection.value;
                    instrumentInput.value = selection;
                }
            }
        }
      });
}

// 🔗 open element href in a modal dialog
function editFile(element)
{
    let dialog = element.nextElementSibling;
    fetch(element.href)
        .then(response => response.text())
        .then(html => {
            dialog.innerHTML = html;
            dialog.showModal();
            AutoComplete();
        })
        .catch(function (err) {
            console.warn('Something went wrong.', err);
        });

    return false;
}

// ❌ close dialog on click outside
document.querySelectorAll('dialog').forEach(dialog => {
    
    // register with polyfill for FF/iOS supporrt
    dialogPolyfill.registerDialog(dialog)

    dialog.addEventListener('click', click => {
        const rect = dialog.getBoundingClientRect();
        if (click.clientY < rect.top || click.clientY > rect.bottom ||
            click.clientX < rect.left || click.clientX > rect.right) {
                dialog.close();
        }
    });

    dialog.addEventListener('submit', submit => {
        submit.preventDefault();

        var form = dialog.querySelector('form');
        var xhr = new XMLHttpRequest();
        xhr.open("POST", form.action);
        xhr.send(new FormData(form));
        document.body.classList.add('loading');
        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4)
                dialog.close();
            document.body.classList.remove('loading');
        };
    });
});

// 🔃 global loading indicator for fetches
var oldFetch = fetch;  
fetch = function(url, options) {
    var promise = oldFetch(url, options);
    document.body.classList.add('loading');
    promise.then(() => { document.body.classList.remove('loading'); });
    return promise;
};

(() => {
    fetch('/logs')
      .then(response => {
        const elem = document.getElementById('log_output');
        const reader = response.body.getReader();
        const readStream = ({ done,value }) => {
          if (done) {
            return;
          }
          let chunk = String.fromCharCode.apply(null, value);
          elem.textContent += chunk + '\n';
          return reader.read().then(readStream);
        };
        reader.read().then(readStream);
      });
})();