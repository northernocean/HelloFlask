// data passed in from flask
var metadata = JSON.parse(view_data);

// fetch csv data and create chart
if (metadata.data_source == "csv-fetch") {
  d3.csv(metadata.uri)
    .then(function (data) {
      console.log(data);
      createPlot(summarizeData(data, dateFormat="mm/dd/yyyy"));
    })
    .catch(function (e) {
      console.log(e);
    });
}

// fetch json data and create chart
if (metadata.data_source == "json-fetch") {
  d3.json(metadata.uri)
    .then(function (data) {
      console.log(data);
      createPlot(summarizeData(data, dateFormat="yyyy-mm-dd"));
    })
    .catch(function (e) {
      console.log(e);
    });
}

function summarizeData(data, dateFormat) {
  years = {};
  const fmt = dateFormat.startsWith("yyyy") ? "ymd" : "dmy";
  data.forEach(function (item) {
    //Json data source has dates in format "yyyy-mm-dd"
    //  but csv data source has dates in format "mm/dd/yyyy"
    if(fmt == "ymd")
      year = item.Date.split("-")[0];
    else
      year = item.Date.split("/")[2];
    console.log(year);
    if (years.hasOwnProperty(year)) {
      years[year] += 1;
    } else {
      years[year] = 1;
    }
  });
  // Sort and sum up count by years
  let sorted_years = Object.keys(years).sort((a, b) => a - b);
  xs = [];
  ys = [];
  sorted_years.forEach(function (key) {
    ys.push(years[key]);
    xs.push(key);
  });
  return { xs: xs, ys: ys };
}

// create plot
function createPlot(data) {
  let trace1 = {
    x: data.xs,
    y: data.ys,
    type: "bar",
  };

  let traces = [trace1];

  let layout = {
    title: "Earthquakes by Year",
  };

  Plotly.newPlot("plot", traces, layout);
}
