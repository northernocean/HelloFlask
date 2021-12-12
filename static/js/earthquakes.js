function createPlot(d) {
  
  var data = JSON.parse(d);
  
  let trace1 = {
    x: data.xs,
    y: data.ys,
    type: 'bar'

  };

  let traces = [trace1];

  let layout = {
    title: "Earthquakes by Year",
    yaxis:{
      showticklabels: false
    }
  };

  Plotly.newPlot("plot", traces, layout);

}