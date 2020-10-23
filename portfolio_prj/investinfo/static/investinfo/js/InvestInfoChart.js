var ctx = document.getElementById('myChart').getContext('2d');

var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: date,
        datasets: [{
            data: adjclose,
            label: labelname,
            borderColor: "#3f51b5",
            fill: false
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Скорректированная цена закрытия акции'
                },
            legend: {
                position: 'top'
            },
            scales: {
                xAxes: [{
                    ticks:{
                        maxRotation: 0,
                        autoSkipPadding: 50,
                        },
                    }],
                yAxes: [{
                    ticks:{
                        padding: 1,
                        lineHeight: 10
                        },
                    }]
                },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x',
                    },
                    zoom: {
                        enabled: true,
                        mode: 'x',
                        speed: 0.001,
                        drag: false
                        }
                    }
                }
            }
    });
