/**
 *  Wordcloud by Alexander Krasnov
 *
 *  Uses D3.js module
 */


// Converts string 'aaa bbb ccc' into 'Aaa bbb ccc'
String.prototype.toCapitalFirst = function() {
    return this[0].toUpperCase() + this.slice(1);
}


// Converts string 'aaa bbb ccc' into 'Aaa Bbb Ccc'
String.prototype.toCapitalEach = function() {
    return this.split(' ').map(s => s.toCapitalFirst()).join(' ');
}


const wc_max = Math.max(...wc_data.map(x => x.count)),
      wc_min = Math.min(...wc_data.map(x => x.count)),
      //wc_colors = d3.schemeGnBu[5],
      //wc_colors = d3.schemeDark2,
      //wc_colors = d3.schemeRdPu[9],
      wc_colors = d3.schemeRdBu[10],
      wordcloud_cont = '#wordcloud-container';


function build_wordcloud(container) {
    const width = d3.select(container).node().getBoundingClientRect().width,
          height = width / 4;
          font_name = 'BenchNine';

    let max_font_size = 90;

    if (width < 1200)
        max_font_size = 80;

    if (width < 900)
        max_font_size = 70;

    if (width < 600)
        max_font_size = 56;

    let layout = d3.layout.cloud()
        .size([width, height])
        .words(wc_data)
        .padding(3)
        // Algorithmes of word rotation depending word size, random values, etc.
        .rotate(function(d) {
            //return ~~(Math.random() * 2) * 90;
            //return Math.round(Math.random() * 90);
            //return (~~(Math.random() * 2) * 90) / (Math.round(Math.random() * 3) + 1);

            if (d.text.length > 8 /*|| d.count / wc_max > 0.33*/)
                return 0;
            else
                return (~~(Math.random() * 6) - 3) * 30;
        })
        .font(font_name)
        // Font size using min-max normalization
        .fontSize(function(d) {
            const o = 0.3,
                  c = (d.count - wc_min) / (wc_max - wc_min) + o,
                  c_max = 1 + o;

            return  max_font_size * c / c_max;
        })
        .on('end', draw);

    layout.start();

    function draw(words) {
        d3.select(container).append('svg')
              .attr('width', layout.size()[0])
              .attr('height', layout.size()[1])
          .append('g')
              .attr('transform', 'translate(' + layout.size()[0] / 2 + ',' + layout.size()[1] / 2 + ')')
          .selectAll('text')
              .data(words)
          .enter().append('text')
              .style('font-size', function(d) {
                  return d.size + 'px';
              })
          // Algorithmes of color calculation
          .style('fill', function(d, i) {
              //return wc_colors[wc_colors.length - Math.round(d.count / wc_max * (wc_colors.length - 1)) - 1];
              return wc_colors[Math.round(Math.random() * (wc_colors.length - 1))];
          })
          .style('font-family', font_name)
          .attr('text-anchor', 'middle')
          .attr('transform', function(d) {
              return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
          })
          .text(function(d) {
              return d.text.toCapitalEach();
          });
    }
}


$(document).ready(function() {
    // Initial build of wordcloud
    build_wordcloud(wordcloud_cont);

    // Let's rebuild wordcloud on window resize event has fired
    $(window).resize(function() {
        $(wordcloud_cont).empty();

        build_wordcloud(wordcloud_cont);
    });

});

