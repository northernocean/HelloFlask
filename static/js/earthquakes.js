// Fetch data from api
view_data = JSON.parse(view_data);

d3.json(
  view_data.url)
  .then(function (data) {
    createPlot(data);
  })
  .catch(function (e) {
    console.log(e);
  });

// create plot
  function createPlot(data) {

  let trace1 = {
    x: data.xs,
    y: data.ys,
    type: 'bar'

  };

  let traces = [trace1];

  let layout = {
    title: "Earthquakes by Year",
  };

  Plotly.newPlot("plot", traces, layout);

}