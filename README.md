# announcements

TODO https://dayalstrub.github.io/announcements/

## Development

### Slides

The revealjs slides are rendered using [quarto](https://quarto.org/): 

```bash
quarto render slides/slides.qmd
```

### App

The streamlit app is deployed using GH Pages and [stlite](https://github.com/whitphx/stlite?tab=readme-ov-file#use-stlite-on-your-web-page-stlitemountable) - a port of Streamlit to Wasm, powered by Pyodide - via the index.html page.
See the stlite README for details on importing data, working with `requests` in Pyodide, etc.
