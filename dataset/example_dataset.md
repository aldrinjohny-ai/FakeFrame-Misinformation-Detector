# Example Dataset Format

This directory is for storing test images and captions for FakeFrame.

## Structure

### Match Examples (Consistent Image-Caption Pairs)

Create subdirectories for different categories:

```
dataset/match_examples/
├── animals/
│   ├── dog_park.jpg
│   ├── dog_park.txt → "A golden retriever playing fetch in the park"
│   ├── cat_sleeping.jpg
│   └── cat_sleeping.txt → "A tabby cat sleeping on a cozy blanket"
│
├── nature/
│   ├── sunset_beach.jpg
│   ├── sunset_beach.txt → "Beautiful sunset over the ocean beach"
│   ├── mountain_view.jpg
│   └── mountain_view.txt → "Snow-capped mountains under blue sky"
│
└── urban/
    ├── city_street.jpg
    ├── city_street.txt → "Busy city street with cars and pedestrians"
    ├── coffee_shop.jpg
    └── coffee_shop.txt → "Interior of a modern coffee shop"
```

### Mismatch Examples (Inconsistent Image-Caption Pairs)

```
dataset/mismatch_examples/
├── wrong_object/
│   ├── dog_image.jpg
│   └── wrong_caption.txt → "A sports car racing on the track"
│
├── wrong_context/
│   ├── beach_image.jpg
│   └── wrong_caption.txt → "Snowy mountain landscape in winter"
│
└── misleading/
    ├── protest_2020.jpg
    └── misleading_caption.txt → "Recent protest from yesterday"
```

## Testing Your Dataset

1. Place image files (.jpg, .png, etc.) in appropriate directories
2. Create corresponding .txt files with the same name containing captions
3. Use the web interface to test each pair
4. Record the similarity scores for analysis

## Expected Results

- **Match examples** should score ≥ 0.30 (typically 0.40-0.70)
- **Mismatch examples** should score < 0.30 (typically 0.05-0.25)

## Tips for Creating Test Cases

1. **Clear Matches**: Use descriptive captions that directly describe image content
2. **Subtle Mismatches**: Test edge cases with partially correct captions
3. **Obvious Mismatches**: Use completely unrelated captions
4. **Ambiguous Cases**: Test captions that could apply to multiple images

## Sample Test Cases

### High Similarity (Match)
- Image: Golden retriever in park
- Caption: "A dog playing outdoors"
- Expected: ~0.55-0.65

### Medium Similarity (Borderline)
- Image: Golden retriever in park
- Caption: "An animal in nature"
- Expected: ~0.30-0.40

### Low Similarity (Mismatch)
- Image: Golden retriever in park
- Caption: "A car on the highway"
- Expected: ~0.05-0.15
