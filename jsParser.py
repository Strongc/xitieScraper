# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


__author__='Xingjian Lin, Guo Zhang'


import re


def parseJS(scriptText):
    
    # dateList
    patternCate = re.compile('categories: \[.*\]')
    patternNumCate = re.compile('\d+\.\d+')
    matchCate = re.search(patternCate, scriptText)
    try:
        cate = matchCate.group(0)
        dateList = re.findall(patternNumCate, cate)
    except:
        dateList = None
    
    # priceList
    patternData = re.compile('data: \[.*\]')
    patternNumData = re.compile('\d+\.\d+')
    matchData = re.search(patternData, scriptText)
    try:
        data = matchData.group(0)
        priceList = re.findall(patternNumData, data)
    except:
        priceList = None
    
    return dateList,priceList


if __name__ == '__main__':
    scriptText = '''
    $(function () {
    $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: '海天味极鲜酱油1.9L 送海天上等蚝油260g 优惠促销装',
            style: {
                color: '#f60',
                fontSize: '16px',
            }
        },
        subtitle: {
            text: '天猫网页编号:41124112598　　　最低价:￥17.50元　　　最高价:￥27.50元　　　西贴网www.XiTie.com从 1970-01-01 开始收录',
            style: {
                color: '#848484',
                fontSize: '14px',
            }
        },
        xAxis: {
            categories: ['02.03','02.29','03.01','03.18','03.20','03.31','04.01','04.30']
        },
        yAxis: {
            title: {
                text: '价格（元）'
            }
        },
        tooltip: {
            enabled: true,
            formatter: function() {
                return '日期:'+this.x +'<br/>'+'价格:'+ this.y +'元';
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        credits: {
        enabled:true,
        href :"http://www.xitie.com",
        text : "西贴 http://www.xitie.com"
        },
        series: [{
            name: 'www.XiTie.com 西贴 - 网上商城历史价格查询',
            data: [19.90,27.50,19.90,17.50,19.90,27.50,19.90,27.50]
        }]
    });
});
    '''
    
    dataList,priceList = parseJS(scriptText)
    print(dataList)
    print(priceList)



    