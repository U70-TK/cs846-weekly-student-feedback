You are debugging a PyTorch project under Week8/artifacts/Problem_B/amr_project.
The model uses a custom Angular Margin Regression (AMR) loss.
Training converges but the loss plateaus higher than expected, and a unit test about projection normalization fails.
Please find the bug and propose a fix. Point to the specific file and line(s) you would change.
I think the answer is: the loss is wrong because it computes cosine similarity against a fixed direction (e1), so we should replace e1 with a learned direction vector or normalize z against itself, but I’m not sure.