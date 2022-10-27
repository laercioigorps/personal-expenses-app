/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')

  var ctxP = document.getElementById("pieChart").getContext('2d');
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })


  var myPieChart = new Chart(ctxP, {
      type: 'pie',
      data: {
        labels: ["Red", "Green", "Yellow", "Grey", "Dark Grey"],
        datasets: [{
          data: [300, 50, 100, 40, 120],
          backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
          hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
        }]
      },
      options: {
        responsive: true
      }
    })

$(".fab,.backdrop").click(function(){
    if($(".backdrop").is(":visible")){
      $(".backdrop").fadeOut(125);
      $(".fab.child")
        .stop()
        .animate({
          bottom  : $("#masterfab").css("bottom"),
          opacity : 0
        },125,function(){
          $(this).hide();
        });
    }else{
      $(".backdrop").fadeIn(125);
      $(".fab.child").each(function(){
        $(this)
          .stop()
          .show()
          .animate({
            bottom  : (parseInt($("#masterfab").css("bottom")) + parseInt($("#masterfab").outerHeight()) + 70 * $(this).data("subitem") - $(".fab.child").outerHeight()) + "px",
            opacity : 1
          },125);
      });
    }
  });



})()









