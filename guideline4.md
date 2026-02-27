You are debugging a PyTorch project under Week8/artifacts/Problem_B/amr_project.
The model uses a custom Angular Margin Regression (AMR) loss.
Training converges but the loss plateaus higher than expected, and a unit test about projection normalization fails.
Please find the bug and propose a fix. Point to the specific file and line(s) you would change.
I think the answer is: the issue is in AMRLoss, and we should normalize z inside AMRLoss.forward using F.normalize(z, dim=1) before computing cos_sim, but I’m not sure.