# Research interpretation memo — 2026-10-02

## What the evidence establishes

1. **The interface changes joint-action structure.** In the controlled-initial
   comparison, displaying peer history changes equal-price persistence and
   seller allocation while minimum-price welfare remains nearly fixed. The
   Candidate A replication gives `D_tie=0.830`, with a block-t interval and a
   completion range that remain positive.
2. **The blind spot is structural, not a generic error rate.** Under the
   settlement rule, 100 ordered states collapse into 10 welfare classes.
   Seller-level allocation and equality separate states inside those classes;
   therefore a welfare-only monitor is observationally equivalent on some
   distinct joint states. This is a certificate for the tested settlement, not
   a population-wide false-negative rate.
3. **Structure reaches welfare only under a particular transition direction.**
   Programmed starts mostly resolve ties downward and produce little welfare
   movement. Model-chosen starts can resolve the same welfare-equivalent
   capture state upward into a 6.5 tie, producing a later welfare loss. The
   reversal is descriptive and tied to the different initial-state designs.
4. **Agent class matters.** The tabular Q-learning baseline makes the same
   display manipulation welfare-visible and exhibits a positive-control
   response to a forced deviation. This is a boundary condition on the
   monitor, not evidence that the LLM follows the same policy.

## What the evidence does not establish

- No general claim about collusion, punishment equilibria, or harmful strategic
  coordination is identified.
- The observed 6.0/6.5 ties are above the joint-profit maximum at 5.5, so the
  current operating point cannot separate strategic sustainment from anchoring
  or inertia.
- The data do not justify pooling DeepSeek, Qwen, GLM or other model families;
  the confirmatory estimand is conditional on the tested deployment.
- The amended closed-loop runs and post-hoc leading-indicator analysis do not
  support a fresh confirmatory causal mediation claim.

## Paper-level contribution

The defensible contribution is a measurement framework and an empirical
demonstration: aggregate welfare can be unchanged while an interface
intervention changes the distribution and allocation of joint actions. The
paper's positive result is therefore an **information-dependent observability
boundary**, not a cartel diagnosis. The settlement certificate, controlled
replication, model-chosen transition analysis and agent-class baseline form a
coherent evidence ladder from arithmetic identification to bounded empirical
behavior.

## If a follow-up strategic study is funded

Register a separate protocol with (i) a target at or below the 5.5 joint-profit
price, (ii) an explicit profitable deviation, (iii) a pre-specified response
window and deterrence criterion, (iv) a positive control, and (v) a model-family
and initial-state plan. Do not append such a run to this manuscript or pool it
with the current observability estimand.
