//threshold plugin
(function(root, factory) {
  if (typeof define === "function" && define.amd) {
    // AMD. Register as an anonymous module.
    define([], function() {
      return (root.returnExportsGlobal = factory());
    });
  } else if (typeof exports === "object") {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like enviroments that support module.exports,
    // like Node.
    module.exports = factory();
  } else {
    root["Chartist.plugins.ctThreshold"] = factory();
  }
})(this, function() {
  /**
   * Chartist.js plugin to display a data label on top of the points in a line chart.
   *
   */
  /* global Chartist */
  (function(window, document, Chartist) {
    "use strict";

    var defaultOptions = {
      bisect: "X",
      threshold: 0,
      classNames: {
        aboveThreshold: "ct-threshold-above",
        belowThreshold: "ct-threshold-below"
      },
      maskNames: {
        aboveThreshold: "ct-threshold-mask-above",
        belowThreshold: "ct-threshold-mask-below"
      }
    };

    function createMasks(data, options) {
      // Select the defs element within the chart or create a new one
      var defs = data.svg.querySelector("defs") || data.svg.elem("defs");
      // x1,y1 = bottom left / x2,y2 = top right
      // Project the threshold value on the chart X or Y axis
      var bisectX = options.bisect == "X";
      var bisectY = options.bisect == "Y";
      var projectedThresholdY = bisectY
        ? data.chartRect.height() -
          data.axisY.projectValue(options.threshold) +
          data.chartRect.y2
        : 0;
      var projectedThresholdX = bisectX
        ? data.chartRect.width() -
          data.axisX.projectValue(options.threshold) +
          data.chartRect.y2
        : 0;

      console.log(data);
      console.log("xWidth " + data.chartRect.width());
      console.log(
        "xProjectValue " + data.axisX.projectValue(options.threshold)
      );

      var width = data.svg.width();
      var height = data.svg.height();

      console.log("height " + height);
      console.log("width " + width);

      var aboveThresholdY = height - projectedThresholdY;
      var aboveThresholdX = width - projectedThresholdX;

      console.log("x " + projectedThresholdX + ", y " + projectedThresholdY);

      console.log("aboveX" + aboveThresholdX);
      console.log("aboveY" + aboveThresholdY);

      // Create mask for part above threshold
      defs
        .elem("mask", {
          x: 0,
          y: 0,
          width: width,
          height: height,
          id: options.maskNames.aboveThreshold
        })
        .elem("rect", {
          x: 0,
          y: 0,
          width: aboveThresholdX || width,
          height: projectedThresholdY || height,
          fill: "white"
        });
      
        data.svg
        .elem("svg", {
          x: aboveThresholdX,
          y: 0,
          width: width,
          height: height
        })
        .elem("line", {
          x1: 0,
          x2: 0,
          y1: 0,
          y2: height - data.options.chartPadding.bottom,
          "stroke-width": 2,
          stroke: "black",
          "stroke-dasharray": 5
        });
      
        // x=width/2 + 25
        data.svg.foreignObject(`<span>Threshold ${options.threshold}%</span>`, {
          x:aboveThresholdX - 50, // should really get width of word and divide by two, not use 50 as hardcoded value
          width: width
        },
        "test-threshold-title"
        );
      

      // Create mask for part below threshold
      defs
        .elem("mask", {
          x: 0,
          y: 0,
          width: aboveThresholdX || width,
          height: height,
          id: options.maskNames.belowThresholdX
        })
        .elem("rect", {
          x: projectedThresholdX,
          y: projectedThresholdY,
          width: bisectX ? projectedThresholdX : width,
          height: bisectY ? aboveThresholdY : height,
          fill: "white"
        });
      
      // Add threshold above threshold line
      // const title = new Chartist.Svg("text");
      // title.addClass('threshold-title');
      // title.text('Threshold ' + options.threshold + '%');
      // title.attr({
      //   x: aboveThresholdX - 20,
      //   y: 20,
      // //   transform: transform,
      // //   "text-anchor": options.axisY.textAnchor
      // });
      // data.svg.append(title, true);

      return defs;
    }

    Chartist.plugins = Chartist.plugins || {};
    Chartist.plugins.ctThreshold = function(options) {
      options = Chartist.extend({}, defaultOptions, options);

      var thresholdAxis = options.bisect === "Y" ? "y" : "x";

      return function ctThreshold(chart) {
        if (chart instanceof Chartist.Line || chart instanceof Chartist.Bar) {
          chart.on("draw", function(data) {
            if (data.type === "point") {
              // For points we can just use the data value and compare against the threshold in order to determine
              // the appropriate class
              data.element.addClass(
                data.value[thresholdAxis] >= options.threshold
                  ? options.classNames.aboveThreshold
                  : options.classNames.belowThreshold
              );
            } else if (
              data.type === "line" ||
              data.type === "bar" ||
              data.type === "area"
            ) {
              // Cloning the original line path, mask it with the upper mask rect above the threshold and add the
              // class for above threshold
              data.element
                .parent()
                .elem(data.element._node.cloneNode(true))
                .attr({
                  mask: "url(#" + options.maskNames.aboveThreshold + ")"
                })
                .addClass(options.classNames.aboveThreshold);

              // Use the original line path, mask it with the lower mask rect below the threshold and add the class
              // for blow threshold
              data.element
                .attr({
                  mask: "url(#" + options.maskNames.belowThreshold + ")"
                })
                .addClass(options.classNames.belowThreshold);
            }
          });

          // On the created event, create the two mask definitions used to mask the line graphs
          chart.on("created", function(data) {
            createMasks(data, options);
          });
        }
      };
    };
  })(window, document, Chartist);

  return Chartist.plugins.ctThreshold;
});