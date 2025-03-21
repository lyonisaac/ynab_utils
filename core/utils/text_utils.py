"""Text processing utilities."""
import re
from typing import Optional, List


def has_emoji(text: str) -> bool:
    """
    Check if text contains an emoji.
    
    Args:
        text: String to check for emoji
        
    Returns:
        bool: True if emoji found, False otherwise
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002300-\U000023FF"  # Miscellaneous Technical
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "\U0000FE00-\U0000FE0F"  # Variation Selectors
        "\U000024C2-\U0001F251"
        "\u200d"  # Zero width joiner
        "\u20D0-\u20FF"  # Combining Diacritical Marks for Symbols
        "]+"
    )
    return bool(emoji_pattern.search(text))


def extract_emojis(text: str) -> List[str]:
    """
    Extract all emojis from text.
    
    Args:
        text: String to extract emojis from
        
    Returns:
        List[str]: List of extracted emojis
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002300-\U000023FF"  # Miscellaneous Technical
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "\U0000FE00-\U0000FE0F"  # Variation Selectors
        "\U000024C2-\U0001F251"
        "\u200d"  # Zero width joiner
        "\u20D0-\u20FF"  # Combining Diacritical Marks for Symbols
        "]+"
    )
    return emoji_pattern.findall(text)


def strip_emoji(text: str) -> str:
    """
    Remove all emojis from text.
    
    Args:
        text: String to remove emojis from
        
    Returns:
        str: Text with emojis removed
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002300-\U000023FF"  # Miscellaneous Technical
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "\U0000FE00-\U0000FE0F"  # Variation Selectors
        "\U000024C2-\U0001F251"
        "\u200d"  # Zero width joiner
        "\u20D0-\u20FF"  # Combining Diacritical Marks for Symbols
        "]+"
    )
    return emoji_pattern.sub(r'', text)