/**
 *  Twitter data visualization by Alexander Krasnov
 *
 *  Uses C3/D3.js module
 */


var color_tw = '#c8102e', // Tweets' color
    color_rt = '#012169', // Retweets' color
    color_ne = '#aaaaaa'; // Neutral color


// Retweets to tweets ratio
var chart1 = c3.generate({
    bindto: '#chart1',
    padding: {
        top: 10,
        bottom: 10,
    },
    data: {
        columns: [
            ['Tweets', ch_data.cnt_tw],
            ['Retweets', ch_data.cnt_rt],
        ],
        type: 'pie',
        colors: {
            'Tweets': color_tw,
            'Retweets': color_rt,
        }
    },
    size: {
        width: 320,
        height: 320
    }
});


// Total tweets and retweets rate
/*
var chart2 = c3.generate({
    bindto: '#chart2',
    padding: {
       top: 10,
       right: 30,
       bottom: 10,
       left: 40
    },
    data: {
        x: 'x',
        xFormat: '%Y-%m-%d %H:%M',
            columns: [
            ['x'].concat(ch_data.ts1_chart['dtm']),
            ['Total tweet rate'].concat(ch_data.ts1_chart['val']),
        ],
        point: {
            show: false
        }
    },
    color: {
        pattern: [color_ne]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%b %d, %H:%M',
                count: 20
            }
        }
    },
    grid: {
        x: {
            show: true
        }
    }
});
*/


// Tweets vs retweets rate
var chart3 = c3.generate({
    bindto: '#chart3',
    padding: {
        top: 10,
        right: 30,
        bottom: 10,
        left: 40
    },
    size: {
        height: 400,
    },
    data: {
        x: 'x',
        xFormat: '%Y-%m-%d %H:%M',
        columns: [
            ['x'].concat(ch_data.ts2_chart['dtm']),
            ['Tweet rate'].concat(ch_data.ts2_chart['val_tw']),
            ['Retweet rate'].concat(ch_data.ts2_chart['val_rt']),
            ['Total tweet rate'].concat(ch_data.ts1_chart['val']),
        ],
        types: {
            'Tweet rate': 'spline',
            'Retweet rate': 'spline',
            'Total tweet rate': 'area-spline'
        }
    },
    tooltip: {
        format: {
            value: function(value) {
                return value.toLocaleString()
            }
        }
    },
    point: {
        show: false
    },
    color: {
        pattern: [color_tw, color_rt, color_ne]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d %H:%M',
                count: 20
            }
        }
    },
    grid: {
        x: {
            show: true
        }
    }
});


// Top retweeters including bots
var chart4 = c3.generate({
    bindto: '#chart4',
    padding: {
        top: 10,
        right: 10,
        bottom: 10,
        left: 100
    },
    bar: {
        width: 12
    },
    data: {
        x: 'Username',
        columns: [
            ['Username'].concat(ch_data.top_rt_bots['users']),
            ['Retweets'].concat(ch_data.top_rt_bots['tweets'])
        ],
        type: 'bar',
        groups: [
            ['Top retweeters inc. bots']
        ]
    },
    tooltip: {
        format: {
            value: function(value) {
                return value.toLocaleString()
            }
        }
    },
    legend: {
        show: true
    },
    axis: {
        rotated: true,
        x: {
            type: 'category'
        }
    },
    color: {
        pattern: [color_rt]
    },
    grid: {
        y: {
            show: true
        }
    }
});


// Top tweeters including bots
var chart5 = c3.generate({
    bindto: '#chart5',
    padding: {
        top: 10,
        right: 10,
        bottom: 10,
        left: 100
    },
    bar: {
        width: 12
    },
    data: {
        x: 'Username',
        columns: [
            ['Username'].concat(ch_data.top_tw_bots['users']),
            ['Tweets'].concat(ch_data.top_tw_bots['tweets'])
        ],
        type: 'bar',
        groups: [
            ['Top tweeters inc. bots']
        ]
    },
    tooltip: {
        format: {
            value: function(value) {
                return value.toLocaleString()
            }
        }
    },
    legend: {
        show: true
    },
    axis: {
        rotated: true,
        x: {
            type: 'category'
        }
    },
    color: {
        pattern: [color_tw]
    },
    grid: {
        y: {
            show: true
        }
    }
});


// Top 10 retweeters w/o bots -- retweets by tweets 
var chart6 = c3.generate({
    bindto: '#chart6',
    padding: {
        top: 10,
        right: 10,
        bottom: 10,
        left: 100
    },
    bar: {
        width: 12
    },
    data: {
        x: 'Username',
        columns: [
            ['Username'].concat(ch_data.top_10_rt['users']),
            ['Retweets'].concat(ch_data.top_10_rt['tweets']),
            ['Tweets'].concat(ch_data.top_10_rt_tw['tweets'])
        ],
        type: 'bar',
        groups: [
            ['Retweets', 'Tweets']
        ]
    },
    legend: {
        show: true
    },
    axis: {
        rotated: true,
        x: {
            type: 'category'
        }
    },
    color: {
        pattern: [color_rt, color_tw]
    },
    grid: {
        y: {
            show: true
        }
    }
});


// Top 10 tweeters w/o bots -- tweets by retweets 
var chart7 = c3.generate({
    bindto: '#chart7',
    padding: {
        top: 10,
        right: 10,
        bottom: 10,
        left: 100
    },
    bar: {
        width: 12
    },
    data: {
        x: 'Username',
        columns: [
            ['Username'].concat(ch_data.top_10_tw['users']),
            ['Tweets'].concat(ch_data.top_10_tw['tweets']),
            ['Retweets'].concat(ch_data.top_10_tw_rt['tweets'])
        ],
        type: 'bar',
        groups: [
            ['Tweets', 'Retweets']
        ]
    },
    legend: {
        show: true
    },
    axis: {
        rotated: true,
        x: {
            type: 'category'
        }
    },
    color: {
        pattern: [color_tw, color_rt]
    },
    grid: {
        y: {
            show: true
        }
    }
});


// Geo-location
var chart8 = c3.generate({
    bindto: '#chart8',
    padding: {
        top: 10,
        bottom: 10,
    },
    data: {
        columns: [
            ['Geo-location enabled', ch_data.geo_coded['enabled']],
            ['Geo-location disabled', ch_data.geo_coded['disabled']],
        ],
        type: 'pie',
        size: {
            width: 200,
            height: 300
        },
        colors: {
            'Geo-location enabled': color_tw,
            'Geo-location disabled': color_rt,
        }
    }
});


// Profile location
var chart9 = c3.generate({
    bindto: '#chart9',
    padding: {
        top: 10,
        bottom: 10,
    },
    data: {
        columns: [
            ['Profile location set', ch_data.have_location['yes']],
            ['Profile location not set', ch_data.have_location['no']],
        ],
        type: 'pie',
        size: {
            width: 200,
            height: 300
        },
        colors: {
            'Profile location set': color_tw,
            'Profile location not set': color_rt,
        }
    }
});


// Tweet vs Retweet volumes
var chart10 = c3.generate({
    bindto: '#chart10',
    padding: {
        top: 10,
        right: 20,
        bottom: 10,
        left: 40
    },
    bar: {
        width: 20
    },
    data: {
        x: 'Number of tweets',
        columns: [
            ['Number of tweets'].concat(ch_data.volumes['number']),
            ['Users tweeting this many times'].concat(ch_data.volumes['tweeters']),
            ['Users retweeting this many times'].concat(ch_data.volumes['retweeters'])
        ],
        type: 'bar',
        groups: [
            ['Users tweeting this many times', 'Users retweeting this many times']
        ]
    },
    tooltip: {
        format: {
            value: function(value) {
                return value.toLocaleString()
            }
        }
    },
    legend: {
        show: true
    },
    axis: {
        rotated: true,
        x: {
            type: 'category',
        },
        y: {
            tick: {
                format: function(value) {
                    return value.toLocaleString();
                }
            }
        }
    },
    color: {
        pattern: [color_tw, color_rt]
    },
    grid: {
        y: {
            show: true
        }
    }
});


// Histogram (hashtags)
var chart11 = c3.generate({
    bindto: '#chart11',
    padding: {
        top: 10,
        right: 0,
        bottom: 10,
        left: 100
    },
    bar: {
        width: 15
    },
    data: {
        x: 'Hashtags',
        columns: [
            ['Hashtags'].concat(ch_data.hashtags.tags.slice(0, -1)),
            ['Users using this many times'].concat(ch_data.hashtags.count.slice(0, -1)),
        ],
        type: 'bar',
    },
    tooltip: {
        format: {
            value: function(value) {
                return value.toLocaleString()
            }
        }
    },
    legend: {
        show: true
    },
    axis: {
        rotated: true,
        x: {
            type: 'category'
        },
        y: {
            tick: {
                format: function(value) {
                    return value.toLocaleString();
                }
            }
        }
    },
    color: {
        pattern: ['#243a83']
    },
    grid: {
        y: {
            show: true
        }
    }
});


// Donut (hashtags %)
var pie_data = [],
    pie_colors = [];

for(var i=0; i < ch_data.hashtags.tags.length; i++) {
    pie_data[i] = [ch_data.hashtags.tags[i],  ch_data.hashtags.count[i]];
    pie_colors[ch_data.hashtags.tags[i]] = 'rgba(36,58,131,' + (1 - i/15).toFixed(2) + ')';
}

var chart = c3.generate({
    bindto: '#chart12',
    padding: {
        top: 10,
        right: 40,
        bottom: 10,
        left: 0
    },
    data: {
        columns: pie_data,
        colors: pie_colors,
        type : 'donut',
    },
    donut: {
        title: "Top-10 hashtags, %"
    }
});


// Top retweeting bots
for(const rtb of ch_data.top_rt_bot_list) {
    $('#top_rt_bot_list').append(
        '<a href="https://twitter.com/' + rtb.slice(1) + '">' + rtb + '</a> '
    );
}


// Top tweeting bots
for(const twb of ch_data.top_tw_bot_list) {
    $('#top_tw_bot_list').append(
        '<a href="https://twitter.com/' + twb.slice(1) + '">' + twb + '</a> '
    );
}


// What were people sharing
for(const tr in ch_data.top_retweets.text) {
    let t = ch_data.top_retweets.text[tr].replace(/(https\:\/\/t\.co\/[\w\d]+)/, ' →&nbsp;<a href="$1" target="_blank" rel="nofollow">$1</a>');

    t = t.replace(/#([\w\d]+)/g, '<a href="https://twitter.com/hashtag/$1?src=hashtag_click" target="_blank" rel="nofollow">#$1</a>');
    t = t.replace(/@([\w\d]+):/, '<a href="https://twitter.com/$1" target="_blank" rel="nofollow">@$1</a>:');

    const c = ch_data.top_retweets.count[tr].toLocaleString();

    $('#top-retweets').append(
        `<tr><td>${t}</td><td>${c}</td></tr>`
    );
}


// Top-10 users
for(const tu in ch_data.top_10_popular.users) {
    const u = ch_data.top_10_popular.users[tu];

    $('#top-users').append(
        '<tr><td><a href="https://twitter.com/' + u.slice(1) + '" target="_blank" rel="nofollow">' + u + '</a></td>'+
            '<td>' + ch_data.top_10_popular.followers[tu].toLocaleString() + '</td>'+
            '<td>' + ch_data.top_10_popular.friends[tu].toLocaleString() + '</td></tr>'
    );
}


// Top mentions
for(const tm in ch_data.mentions.users.slice(0, -1)) {
    const u = ch_data.mentions.users[tm];

    $('#top-mentions').append(
        '<tr><td><a href="https://twitter.com/' + u.slice(1) + '" target="_blank" rel="nofollow">' + u + '</a></td>'+
            '<td>' + ch_data.mentions.count[tm].toLocaleString() + '</td>' +
            '<td>' + ch_data.mentions.percent[tm] + '%</td></tr>'
    );
}
