# optimal-injection-schedule
This simulation determines the most optimal dosage schedule for multiple people
safely sharing a multi-use medication vial. This program was written more as a
mental exercise than as a practical application to patients or caregivers. It
is generally not accepted that patients should share medication from the same
vial due to the risk of contamination. However, I thought it would be fun to
make an optimization-oriented program.

The premise is that the medication is used safely by multiple people, and that
they each take a constant, recurring dosage over time. If there is not enough
medication left in the vial at the time of an injection, it is thrown away and
considered wasted medication. Another vial is opened, and the simulation
continues.

This simulation considers a range of possible doses and days between doses,
determined by the user-specified parameters, for each person listed. It
considers every possible permutation of doses, within these parameters, so as
to minimize total medication waste. When the simulation is concluded, it
displays the most optimal outcomes.
