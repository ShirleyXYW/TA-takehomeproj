# TA-takehomeproj
The completed take home project of Together AI
Application
• Build an application that implements the following usage:
     $./key-server.go --help
     Usage of ./key-server:
       -max-size size
         maximum key size (default 1024)
       -srv-port port
         server listening port (default 1123)
• It listens on a port, specified by srv-port command-line arg
• Users can send HTTP requests like http://host:port/key/<length>
• On a user GET query, generate a number of random bytes equal to the length requested
• The request may not exceed maximum size, specified by max-size command-line arg
• In the event of invalid input or another fault, the application should return an appropriate HTTP status response (400, 404, 500, etc.)
1
 • Instrument the server with Prometheus metrics including:
– key length distribution histogram, 20 linear buckets from 0 to max-size
– counter of http status codes
• Create at least one positive and one negative unit test
Packaging
• Create a Dockerfile to create a container image
Deployment
• Create a kubernetes deployment helm chart
– allow configuring max size and server port – include liveness/readiness checks
– include reasonable resource claims
Monitoring
• Propose a method by which to notify and alert on any undesired behavior
