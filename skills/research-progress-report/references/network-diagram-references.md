# Network Diagram References

Use these verified original-paper figures as examples of clear architecture communication, then draw the project's actual implementation. The reference figure's layers, dimensions, connections and operation order are not evidence about the current model. Cite the paper and figure used for visual inspiration in the report caption; distinguish a redrawn project architecture from a reproduced source figure.

| Original paper | Verified figures | Useful visual convention |
|---|---|---|
| He et al., *Deep Residual Learning for Image Recognition*, CVPR 2016 — [original PDF](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf) | Fig. 2; Fig. 5 | Fig. 2 separates the residual branch, identity shortcut and elementwise addition. Fig. 5 expands basic and bottleneck blocks with kernel/channel labels. Useful for residual paths, custom blocks and architecture modifications. |
| Ronneberger et al., *U-Net: Convolutional Networks for Biomedical Image Segmentation*, 2015 — [original PDF](https://arxiv.org/pdf/1505.04597) | Fig. 1 | Places channel counts and spatial dimensions on feature maps and uses a legend for convolution, pooling, upsampling and copy-and-crop. Useful for encoder–decoder stages, multiscale fusion and segmentation. |
| Vaswani et al., *Attention Is All You Need*, NIPS 2017 — [original PDF](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) | Fig. 1; Fig. 2 | Pairs a whole-model view with attention-module expansion; shows repeated layers, residual paths, Q/K/V inputs and parallel heads followed by concatenation and output projection. Useful for attention and complex submodules. |
| Hu et al., *Squeeze-and-Excitation Networks*, 2017 preprint, later CVPR 2018 — [original PDF, arXiv v1](https://arxiv.org/pdf/1709.01507v1) | Fig. 1 in this pinned version | Shows feature tensors, spatial squeeze, channel excitation and scaling in one path. Useful for explaining gates, broadcast weights and custom attention/recalibration modules. |

## Adapt the convention to the actual model

Use an overall architecture view to locate the module, and an internal expansion to explain unfamiliar/custom or materially modified computation. Show data direction, input/output meanings, key tensor shapes and layout, repetition, branches and merge operations. Name addition, concatenation and multiplication explicitly; include projections, resizing, cropping, reshape and broadcast when they make the connection valid. Define arrow styles and any distinction between training and inference.

Borrow only the relevant convention. For example, do not insert U-Net's original copy-and-crop into a same-padding implementation, or the original Transformer's normalization placement into a pre-normalized implementation. A proposed architecture should be labeled proposed; unknown operations or dimensions should remain unresolved. Figure, prose, equations and actual implementation must agree.

Read the original figure and caption before citing a new or changed reference; verify its exact version and figure number rather than relying on search thumbnails, secondary redrawings or memory. Prefer a small number of structurally relevant references over an unrelated gallery. Do not imply a custom module was validated just because it resembles a classic diagram.
