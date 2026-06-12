import torch
import segmentation_models_pytorch as smp

def create_segmentation_model(model_name="unetplusplus", encoder_name="resnet34", num_classes=6):
    """
    Creates a segmentation model for DR lesion detection.
    Lesions: Microaneurysms, Hemorrhages, Hard Exudates, Soft Exudates, Cotton Wool Spots, Neovascularization
    """
    if model_name.lower() == "unetplusplus":
        return smp.UnetPlusPlus(
            encoder_name=encoder_name,
            encoder_weights="imagenet",
            in_channels=3,
            classes=num_classes,
        )
    elif model_name.lower() == "deeplabv3plus":
        return smp.DeepLabV3Plus(
            encoder_name=encoder_name,
            encoder_weights="imagenet",
            in_channels=3,
            classes=num_classes,
        )
    elif model_name.lower() == "attention_unet":
        # Using standard Unet as base, but SMP doesn't have an exact Attention Unet class out of the box,
        # so we default to a standard Unet for this placeholder or a custom implementation could go here.
        # DeepLabV3+ and Unet++ are generally stronger anyway.
        return smp.Unet(
            encoder_name=encoder_name,
            encoder_weights="imagenet",
            in_channels=3,
            classes=num_classes,
            decoder_attention_type='scse' # Spatial and Channel Squeeze & Excitation
        )
    else:
        raise ValueError(f"Unknown model name {model_name}")

if __name__ == "__main__":
    model = create_segmentation_model("unetplusplus", "efficientnet-b3", 6)
    dummy_input = torch.randn(2, 3, 512, 512)
    out = model(dummy_input)
    print("Segmentation Model Output Shape:", out.shape)
