# A8 offline prompt-difference diagnostic

This analysis used no provider calls. It compares round-1 natural-display
requests from the four-arm model-chosen-start run with the controlled-initial
HH natural-display run.

The four-arm sample contains 94 natural round-1 requests: 6 HH, 38 LL, 25 LH,
and 25 HL initial histories. The controlled comparison contains 74 HH-natural
requests. Because the four-arm run chooses its initial state, most raw request
differences are the initial-state history itself.

Among the six four-arm requests with the same HH history as the controlled
reference, the system message, model options, tool schema, temperature, token
budget, and structured user payload agree. The only residual difference is
integer-versus-float rendering in the textual constraint (`2` versus `2.0`).

The diagnostic therefore rules out a hidden prompt-content or prompt-length
explanation conditional on a matched initial state. It does not identify why
matching direction differs between model-chosen and programmed starts; that
comparison remains observational and is reported as a limitation.

The raw request logs remain in the sealed local research record and are not
included here because they contain provider request metadata.
