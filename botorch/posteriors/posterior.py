#! /usr/bin/env python3

r"""
Abstract base module for all botorch posteriors.
"""

from abc import ABC, abstractmethod, abstractproperty
from typing import Optional

import torch
from torch import Tensor


class Posterior(ABC):
    r"""Abstract base class for botorch posteriors."""

    @abstractproperty
    def device(self) -> torch.device:
        r"""The torch device this posterior lives on."""
        pass

    @abstractproperty
    def dtype(self) -> torch.dtype:
        r"""The torch dtype of this posterior."""
        pass

    @abstractproperty
    def event_shape(self) -> torch.Size:
        r"""The event shape (i.e. the shape of a single sample)."""
        pass

    @property
    def batch_shape(self) -> torch.Size:
        r"""The t-batch shape."""
        return self.event_shape[:-2]

    @property
    def mean(self) -> Tensor:
        r"""The mean of the posterior as a `(b) x n x o`-dim Tensor."""
        raise NotImplementedError(
            f"Property `mean` not implemented for {self.__name__}"
        )

    @property
    def variance(self) -> Tensor:
        r"""The variance of the posterior as a `(b) x n x o`-dim Tensor."""
        raise NotImplementedError(
            f"Property `variance` not implemented for {self.__name__}"
        )

    @abstractmethod
    def rsample(
        self,
        sample_shape: Optional[torch.Size] = None,
        base_samples: Optional[Tensor] = None,
    ) -> Tensor:
        r"""Sample from the posterior (with gradients).

        Args:
            sample_shape: A `torch.Size` object specifying the sample shape. To
                draw `n` samples, set to `torch.Size([n])`. To draw `b` batches
                of `n` samples each, set to `torch.Size([b, n])`.
            base_samples: An (optional) Tensor of `N(0, I)` base samples of
                appropriate dimension, typically obtained from a `Sampler`.
                This is used for deterministic optimization.

        Returns:
            A `sample_shape x event`-dim Tensor of samples from the posterior.
        """
        pass

    def sample(
        self,
        sample_shape: Optional[torch.Size] = None,
        base_samples: Optional[Tensor] = None,
    ) -> Tensor:
        r"""Sample from the posterior (without gradients).

        This is a simple wrapper calling `rsample` using `with torch.no_grad()`.

        Args:
            sample_shape: A `torch.Size` object specifying the sample shape. To
                draw `n` samples, set to `torch.Size([n])`. To draw `b` batches
                of `n` samples each, set to `torch.Size([b, n])`.
            base_samples: An (optional) Tensor of `N(0, I)` base samples of
                appropriate dimension, typically obtained from a `Sampler`.
                This is used for deterministic optimization.

        Returns:
            A `sample_shape x event`-dim Tensor of samples from the posterior.
        """
        with torch.no_grad():
            return self.rsample(sample_shape=sample_shape, base_samples=base_samples)
