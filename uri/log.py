import log

from uri import config


urilog = log.Log(config.log)
httplog = log.HTTPLog(config.log, config.httplog)
