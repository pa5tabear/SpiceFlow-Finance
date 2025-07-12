| A                                              | B                                                              | C                                        |
|:-----------------------------------------------|:---------------------------------------------------------------|:-----------------------------------------|
| SPICEFLOW FINANCE - SOLAR LEASE NPV CALCULATOR |                                                                |                                          |
|                                                |                                                                |                                          |
| INPUT PARAMETERS                               |                                                                |                                          |
| Annual Base Rent ($)                           | 95680                                                          | ← Enter lease annual rent                |
| Years Remaining                                | 23                                                             | ← Enter remaining lease term             |
| Annual Escalator (%)                           | 0.025                                                          | ← Enter annual escalation %              |
| Risk Tier                                      | Medium                                                         | ← Enter: Low, Medium, or High            |
|                                                |                                                                |                                          |
| RISK TIER LOOKUP                               | Discount Rate                                                  | Description                              |
| Low Risk (Operating + Strong Dev)              | 8%                                                             | Operating project, strong developer      |
| Medium Risk (Construction + Mid-tier)          | 12%                                                            | Under construction, mid-tier dev         |
| High Risk (Development + Weak Dev)             | 16%                                                            | Development stage, unknown dev           |
|                                                |                                                                |                                          |
| CASH FLOW PROJECTION                           |                                                                |                                          |
| Year                                           | Annual Rent                                                    | Present Value                            |
| 1                                              | =B4*(1+B6)^(A16-1)                                             | =B16/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A16 |
| 2                                              | =B4*(1+B6)^(A16-1)                                             | =B17/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A17 |
| 3                                              | =B4*(1+B6)^(A16-1)                                             | =B18/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A18 |
| 4                                              | =B4*(1+B6)^(A16-1)                                             | =B19/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A19 |
| 5                                              | =B4*(1+B6)^(A16-1)                                             | =B20/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A20 |
| 6                                              | =B4*(1+B6)^(A16-1)                                             | =B21/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A21 |
| 7                                              | =B4*(1+B6)^(A16-1)                                             | =B22/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A22 |
| 8                                              | =B4*(1+B6)^(A16-1)                                             | =B23/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A23 |
| 9                                              | =B4*(1+B6)^(A16-1)                                             | =B24/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A24 |
| 10                                             | =B4*(1+B6)^(A16-1)                                             | =B25/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A25 |
| 11                                             | =B4*(1+B6)^(A16-1)                                             | =B26/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A26 |
| 12                                             | =B4*(1+B6)^(A16-1)                                             | =B27/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A27 |
| 13                                             | =B4*(1+B6)^(A16-1)                                             | =B28/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A28 |
| 14                                             | =B4*(1+B6)^(A16-1)                                             | =B29/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A29 |
| 15                                             | =B4*(1+B6)^(A16-1)                                             | =B30/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A30 |
| 16                                             | =B4*(1+B6)^(A16-1)                                             | =B31/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A31 |
| 17                                             | =B4*(1+B6)^(A16-1)                                             | =B32/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A32 |
| 18                                             | =B4*(1+B6)^(A16-1)                                             | =B33/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A33 |
| 19                                             | =B4*(1+B6)^(A16-1)                                             | =B34/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A34 |
| 20                                             | =B4*(1+B6)^(A16-1)                                             | =B35/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A35 |
| 21                                             | =B4*(1+B6)^(A16-1)                                             | =B36/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A36 |
| 22                                             | =B4*(1+B6)^(A16-1)                                             | =B37/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A37 |
| 23                                             | =B4*(1+B6)^(A16-1)                                             | =B38/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A38 |
| 24                                             | =B4*(1+B6)^(A16-1)                                             | =B39/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A39 |
| 25                                             | =B4*(1+B6)^(A16-1)                                             | =B40/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A40 |
|                                                |                                                                |                                          |
| VALUATION RESULTS                              |                                                                |                                          |
| Total Gross Cash Flows                         | =SUM(B16:B40)                                                  |                                          |
| Net Present Value                              | =NPV(VLOOKUP(B7,B10:C12,2,FALSE),B16:B40)                      | ← Net present value of all payments      |
| Buyout Offer (80% of NPV)                      | =B44*0.8                                                       | ← Our cash offer to landowner            |
| Effective Multiple (x Annual Rent)             | =B45/B4                                                        | ← Multiple of current annual rent        |
|                                                |                                                                |                                          |
| VALIDATION BENCHMARKS                          |                                                                |                                          |
| Renewa Benchmark (12.5x Annual)                | =B4*12.5                                                       | ← Industry standard benchmark            |
| Our Multiple vs Renewa                         | =B46/B49                                                       | ← How competitive our offer is           |
| Deal Quality Rating                            | =IF(B50>=0.8,"Competitive",IF(B50>=0.6,"Fair","Below Market")) | ← Deal assessment vs market              |