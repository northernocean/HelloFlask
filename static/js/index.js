function createPlot(data) {
  
  var data = JSON.parse(view_data);
  let trace1 = {
    x: data.xs,
    y: data.ys,
    type: 'bar'

  };

  let traces = [trace1];

  let layout = {
    title: "A Plotly plot"
  };

  Plotly.newPlot("plot", traces, layout);

}