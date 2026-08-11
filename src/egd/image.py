# /egd/image.py

import torch
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import font_manager
from egd.configs.enum import AnatomyClass, DiseaseClass
from egd.configs.constant import ANATOMICAL_CLASSES_LABELS_EN, ANATOMICAL_CLASSES_LABELS_KR, DISEASE_CLASSES_LABELS_EN, DISEASE_CLASSES_LABELS_KR


def _configure_korean_font() -> None:
    """Prefer a Hangul-capable font so Korean labels render without glyph warnings."""
    preferred = (
        "Noto Sans CJK KR",
        "Noto Sans CJK JP",
        "NanumGothic",
        "Malgun Gothic",
        "AppleGothic",
    )
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in available:
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return


_configure_korean_font()


class EGDImage:
    def __init__(self,
        image_path: Path,
        original_image: Image.Image,
        preprocssed_image: torch.Tensor,
        anatomical_classes: list[AnatomyClass],
        disease_classes: list[DiseaseClass],
        anatomical_probabilities: list[float],
        disease_probabilities: list[float],
        anatomical_index: int,
        disease_index: int,
        mean: list[float],
        std: list[float],
    ):
        self.image_path = image_path
        self.original_image = original_image
        self.preprocssed_image = preprocssed_image
        self.anatomical_classes = anatomical_classes
        self.disease_classes = disease_classes
        self.anatomical_probabilities = anatomical_probabilities
        self.disease_probabilities = disease_probabilities
        self.anatomical_index = anatomical_index
        self.disease_index = disease_index
        self.mean = mean
        self.std = std

    def get_anatomical_class(self) -> AnatomyClass:
        return self.anatomical_classes[self.anatomical_index]

    def get_disease_class(self) -> DiseaseClass:
        return self.disease_classes[self.disease_index]

    def get_anatomical_probability(self) -> float:
        return self.anatomical_probabilities[self.anatomical_index]

    def get_disease_probability(self) -> float:
        return self.disease_probabilities[self.disease_index]
    
    def get_result(self) -> dict:
        return {
            "anatomical_class": self.get_anatomical_class(),
            "disease_class": self.get_disease_class(),
            "anatomical_probability": self.get_anatomical_probability(),
            "disease_probability": self.get_disease_probability(),
        }

    def _preprocessed_to_display(self):
        x = self.preprocssed_image.detach().cpu().squeeze(0)
        mean = torch.tensor(self.mean, dtype=x.dtype).view(3, 1, 1)
        std = torch.tensor(self.std, dtype=x.dtype).view(3, 1, 1)
        x = (x * std + mean).clamp(0, 1)
        return x.permute(1, 2, 0).numpy()

    @staticmethod
    def _plot_probability_bars(
        ax,
        labels: list[str],
        probabilities: list[float],
        predicted_index: int,
        title: str,
    ) -> None:
        # Highest probability first so the top of the chart is easy to scan.
        order = sorted(range(len(probabilities)), key=lambda i: probabilities[i], reverse=True)
        labels = [labels[i] for i in order]
        probabilities = [probabilities[i] for i in order]
        predicted_rank = order.index(predicted_index)

        y = range(len(labels))
        colors = [
            "#1f6feb" if i == predicted_rank else "#c5ccd6"
            for i in y
        ]
        bars = ax.barh(y, probabilities, color=colors, height=0.72, zorder=2)
        ax.set_yticks(list(y))
        ax.set_yticklabels(labels, fontsize=9)
        for tick_label, i in zip(ax.get_yticklabels(), y):
            if i == predicted_rank:
                tick_label.set_fontweight("bold")
                tick_label.set_color("#1f6feb")
        ax.set_xlabel("Probability", fontsize=9)
        ax.set_xlim(0, 1.08)
        ax.set_title(title, fontsize=11, pad=8)
        ax.invert_yaxis()
        ax.xaxis.grid(True, linestyle="--", alpha=0.35, zorder=0)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for i, (bar, prob) in enumerate(zip(bars, probabilities)):
            ax.text(
                min(prob + 0.015, 1.02),
                bar.get_y() + bar.get_height() / 2,
                f"{prob:.2f}",
                va="center",
                ha="left",
                fontsize=9,
                fontweight="bold" if i == predicted_rank else "normal",
            )

    def _build_result_figure(self, preprocessed_image: bool = True):
        title = (
            f"{self.image_path.name}\n"
            f"anatomical_class: {ANATOMICAL_CLASSES_LABELS_EN[self.get_anatomical_class()]} / {ANATOMICAL_CLASSES_LABELS_KR[self.get_anatomical_class()]}"
            f"({self.get_anatomical_probability():.2f})\n"
            f"disease_class: {DISEASE_CLASSES_LABELS_EN[self.get_disease_class()]} / {DISEASE_CLASSES_LABELS_KR[self.get_disease_class()]}"
            f"({self.get_disease_probability():.2f})"
        )

        # Short axis labels; full bilingual names stay in the title for the top prediction.
        anat_labels = [ANATOMICAL_CLASSES_LABELS_KR[c] for c in self.anatomical_classes]
        disease_labels = [DISEASE_CLASSES_LABELS_KR[c] for c in self.disease_classes]

        if preprocessed_image:
            fig = plt.figure(figsize=(15, 11), constrained_layout=True)
            gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.45], hspace=0.12, wspace=0.25)
            ax_orig = fig.add_subplot(gs[0, 0])
            ax_prep = fig.add_subplot(gs[0, 1])
            ax_anat = fig.add_subplot(gs[1, 0])
            ax_dis = fig.add_subplot(gs[1, 1])

            ax_orig.imshow(self.original_image)
            ax_orig.set_title("Original")
            ax_orig.axis("off")

            ax_prep.imshow(self._preprocessed_to_display())
            ax_prep.set_title("Preprocessed")
            ax_prep.axis("off")
        else:
            fig = plt.figure(figsize=(10, 16), constrained_layout=True)
            gs = fig.add_gridspec(
                3, 3,
                height_ratios=[2.0, 1.0, 1.0],
                width_ratios=[0.4, 2.2, 0.4],
                hspace=0.12,
            )
            ax_orig = fig.add_subplot(gs[0, 1])
            ax_anat = fig.add_subplot(gs[1, :])
            ax_dis = fig.add_subplot(gs[2, :])

            ax_orig.imshow(self.original_image)
            ax_orig.set_title("Original", fontsize=11)
            ax_orig.axis("off")
            ax_orig.set_aspect("equal")

        self._plot_probability_bars(
            ax_anat,
            anat_labels,
            self.anatomical_probabilities,
            self.anatomical_index,
            "Anatomical class probabilities",
        )
        self._plot_probability_bars(
            ax_dis,
            disease_labels,
            self.disease_probabilities,
            self.disease_index,
            "Disease class probabilities",
        )

        fig.suptitle(title, fontsize=11)
        return fig

    def display_result(self, preprocessed_image: bool = True) -> None:
        fig = self._build_result_figure(preprocessed_image=preprocessed_image)
        plt.show()
        plt.close(fig)

    def save_result(
        self,
        output_path: Path | None = None,
        preprocessed_image: bool = True,
        dpi: int = 150,
    ) -> Path:
        """Save the result figure as ``*/out/*_out.png`` one level above the image folder."""
        if output_path is None:
            output_dir = self.image_path.parent.parent / "out"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{self.image_path.stem}_out.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        fig = self._build_result_figure(preprocessed_image=preprocessed_image)
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return output_path

    def show_image(self) -> None:
        self.original_image.show()
