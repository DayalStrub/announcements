# announcements



## Development

### Slides

The revealjs slides are rendered using [quarto](https://quarto.org/): 

```bash
quarto render slides/slides.qmd
```

### App

The streamlit app (actually [stlite](https://github.com/whitphx/stlite?tab=readme-ov-file#use-stlite-on-your-web-page-stlitemountable) - a port of Streamlit to Wasm, powered by Pyodide) is built locally, converted to HTML at edit.share.stlite.net and then deployed using GH Pages.
