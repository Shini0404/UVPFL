"""
UVPFL Tile Adaptation - Phase 3 of the Algorithm

Implementation of tile-based adaptive streaming as described in the paper:
- VP tiles: Highest quality (viewport)
- VN tiles: Medium quality (neighboring)
- VZ tiles: Low quality (other areas)

Paper Algorithm 1 - Phase 3: Tile Adaptation
"We used a simple hierarchical tile adaptation approach for improved QoE.
The tiles in the coordinate set VP are assigned the highest quality,
the tiles in the coordinate set neighboring viewport VN are assigned medium quality,
and the tiles in the coordinate set VZ are assigned a low quality."
"""

import numpy as np
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from viewport_prediction import (
    Viewport, TileProbabilityCalculator,
    VIDEO_WIDTH, VIDEO_HEIGHT, TILE_SIZE
)


class TileQuality(Enum):
    """Tile quality levels for adaptive streaming."""
    HIGH = "high"       # VP - Viewport tiles
    MEDIUM = "medium"   # VN - Neighboring tiles
    LOW = "low"         # VZ - Other tiles


@dataclass
class TileQualityAssignment:
    """Assignment of quality level to a tile."""
    tile_l: int          # Row index
    tile_k: int          # Column index
    quality: TileQuality
    probability: float   # Visibility probability
    bitrate: int         # Suggested bitrate in kbps


class TileAdapter:
    """
    Tile adaptation for viewport-based streaming.
    
    Implements Phase 3 of UVPFL Algorithm:
    - Assigns quality levels to tiles based on viewport prediction
    - Supports hierarchical quality assignment
    """
    
    # Bitrate settings (typical values for 4K 360° video)
    BITRATE_HIGH = 20000     # 20 Mbps for viewport tiles
    BITRATE_MEDIUM = 5000    # 5 Mbps for neighboring tiles
    BITRATE_LOW = 1000       # 1 Mbps for other tiles
    
    def __init__(self,
                 video_width: int = VIDEO_WIDTH,
                 video_height: int = VIDEO_HEIGHT,
                 tile_size: int = TILE_SIZE,
                 prob_high: float = 0.98,
                 prob_medium: float = 0.95,
                 prob_low: float = 0.90):
        """
        Initialize the tile adapter.
        
        Args:
            video_width: Video width in pixels
            video_height: Video height in pixels
            tile_size: Tile size in pixels
            prob_high: Probability threshold for high quality (>98%)
            prob_medium: Probability threshold for medium quality (>95%)
            prob_low: Probability threshold for low quality (>90%)
        """
        self.video_width = video_width
        self.video_height = video_height
        self.tile_size = tile_size
        self.num_tiles_h = video_width // tile_size
        self.num_tiles_v = video_height // tile_size
        
        self.prob_high = prob_high
        self.prob_medium = prob_medium
        self.prob_low = prob_low
        
        self.tile_calculator = TileProbabilityCalculator(
            video_width, video_height, tile_size
        )
    
    def get_viewport_tiles(self, viewport: Viewport) -> Set[Tuple[int, int]]:
        """Get tiles within the viewport (VP)."""
        tiles = self.tile_calculator.get_viewport_tiles(viewport)
        return set(tiles)
    
    def get_neighboring_tiles(self, 
                              viewport_tiles: Set[Tuple[int, int]],
                              viewport: Viewport) -> Set[Tuple[int, int]]:
        """
        Get tiles neighboring the viewport (VN).
        
        These are tiles adjacent to viewport tiles or with high probability.
        """
        neighboring = set()
        
        # Add adjacent tiles
        for (l, k) in viewport_tiles:
            for dl in [-1, 0, 1]:
                for dk in [-1, 0, 1]:
                    if dl == 0 and dk == 0:
                        continue
                    
                    nl = l + dl
                    nk = (k + dk) % self.num_tiles_h  # Wrap horizontally
                    
                    if 0 <= nl < self.num_tiles_v:
                        if (nl, nk) not in viewport_tiles:
                            neighboring.add((nl, nk))
        
        # Also add high probability tiles
        for l in range(self.num_tiles_v):
            for k in range(self.num_tiles_h):
                if (l, k) in viewport_tiles:
                    continue
                
                prob = self.tile_calculator.calculate_tile_probability(viewport, l, k)
                if prob > self.prob_medium:  # > 95%
                    neighboring.add((l, k))
        
        return neighboring
    
    def assign_quality(self, viewport: Viewport) -> Dict[str, List[TileQualityAssignment]]:
        """
        Assign quality levels to all tiles based on viewport.
        
        Paper Phase 3: Tile Adaptation
        - VP: highest quality (viewport tiles)
        - VN: medium quality (neighboring tiles)
        - VZ: low quality (other tiles)
        
        Args:
            viewport: Current/predicted viewport
            
        Returns:
            Dictionary with 'VP', 'VN', 'VZ' lists of TileQualityAssignment
        """
        # Get tile sets
        vp_tiles = self.get_viewport_tiles(viewport)
        vn_tiles = self.get_neighboring_tiles(vp_tiles, viewport)
        
        assignments = {
            'VP': [],  # Viewport - High quality
            'VN': [],  # Neighboring - Medium quality
            'VZ': []   # Other - Low quality
        }
        
        for l in range(self.num_tiles_v):
            for k in range(self.num_tiles_h):
                prob = self.tile_calculator.calculate_tile_probability(viewport, l, k)
                
                if (l, k) in vp_tiles:
                    assignment = TileQualityAssignment(
                        tile_l=l,
                        tile_k=k,
                        quality=TileQuality.HIGH,
                        probability=prob,
                        bitrate=self.BITRATE_HIGH
                    )
                    assignments['VP'].append(assignment)
                
                elif (l, k) in vn_tiles:
                    assignment = TileQualityAssignment(
                        tile_l=l,
                        tile_k=k,
                        quality=TileQuality.MEDIUM,
                        probability=prob,
                        bitrate=self.BITRATE_MEDIUM
                    )
                    assignments['VN'].append(assignment)
                
                else:
                    assignment = TileQualityAssignment(
                        tile_l=l,
                        tile_k=k,
                        quality=TileQuality.LOW,
                        probability=prob,
                        bitrate=self.BITRATE_LOW
                    )
                    assignments['VZ'].append(assignment)
        
        return assignments
    
    def calculate_bandwidth(self, assignments: Dict[str, List[TileQualityAssignment]]) -> Dict:
        """
        Calculate total bandwidth requirement.
        
        Args:
            assignments: Quality assignments from assign_quality()
            
        Returns:
            Dictionary with bandwidth statistics
        """
        total_bitrate = 0
        
        vp_bitrate = sum(a.bitrate for a in assignments['VP'])
        vn_bitrate = sum(a.bitrate for a in assignments['VN'])
        vz_bitrate = sum(a.bitrate for a in assignments['VZ'])
        
        total_bitrate = vp_bitrate + vn_bitrate + vz_bitrate
        
        # Full quality baseline (all tiles at high quality)
        full_quality_bitrate = (len(assignments['VP']) + len(assignments['VN']) + 
                                len(assignments['VZ'])) * self.BITRATE_HIGH
        
        # Bandwidth savings
        savings = (full_quality_bitrate - total_bitrate) / full_quality_bitrate * 100
        
        return {
            'total_bitrate_kbps': total_bitrate,
            'total_bitrate_mbps': total_bitrate / 1000,
            'vp_bitrate_kbps': vp_bitrate,
            'vn_bitrate_kbps': vn_bitrate,
            'vz_bitrate_kbps': vz_bitrate,
            'full_quality_bitrate_kbps': full_quality_bitrate,
            'bandwidth_savings_percent': savings,
            'num_vp_tiles': len(assignments['VP']),
            'num_vn_tiles': len(assignments['VN']),
            'num_vz_tiles': len(assignments['VZ'])
        }
    
    def get_tiles_to_stream(self, 
                            viewport: Viewport,
                            include_low_quality: bool = True) -> List[Tuple[int, int, int]]:
        """
        Get list of tiles to stream with their bitrates.
        
        Args:
            viewport: Current/predicted viewport
            include_low_quality: Whether to include VZ tiles
            
        Returns:
            List of (tile_l, tile_k, bitrate) tuples
        """
        assignments = self.assign_quality(viewport)
        
        tiles = []
        
        # Always include VP and VN
        for a in assignments['VP']:
            tiles.append((a.tile_l, a.tile_k, a.bitrate))
        
        for a in assignments['VN']:
            tiles.append((a.tile_l, a.tile_k, a.bitrate))
        
        if include_low_quality:
            for a in assignments['VZ']:
                tiles.append((a.tile_l, a.tile_k, a.bitrate))
        
        return tiles


def test_tile_adaptation():
    """Test the tile adaptation system."""
    print("=" * 60)
    print("Testing UVPFL Tile Adaptation (Phase 3)")
    print("=" * 60)
    
    adapter = TileAdapter()
    
    # Test viewport
    viewport = Viewport(yaw=0.0, pitch=0.0, roll=0.0)
    
    print(f"\n1. Viewport: yaw={viewport.yaw}°, pitch={viewport.pitch}°")
    print(f"   FoV: {viewport.h_fov}° x {viewport.v_fov}°")
    
    # Get quality assignments
    print("\n2. Quality Assignment:")
    assignments = adapter.assign_quality(viewport)
    print(f"   VP (High quality): {len(assignments['VP'])} tiles")
    print(f"   VN (Medium quality): {len(assignments['VN'])} tiles")
    print(f"   VZ (Low quality): {len(assignments['VZ'])} tiles")
    
    # Calculate bandwidth
    print("\n3. Bandwidth Analysis:")
    bandwidth = adapter.calculate_bandwidth(assignments)
    print(f"   Total bandwidth: {bandwidth['total_bitrate_mbps']:.1f} Mbps")
    print(f"   Full quality would be: {bandwidth['full_quality_bitrate_kbps']/1000:.1f} Mbps")
    print(f"   Bandwidth savings: {bandwidth['bandwidth_savings_percent']:.1f}%")
    
    # Test different viewports
    print("\n4. Testing different viewports:")
    test_viewports = [
        Viewport(yaw=45.0, pitch=20.0, roll=0.0),
        Viewport(yaw=-90.0, pitch=-10.0, roll=0.0),
        Viewport(yaw=180.0, pitch=30.0, roll=0.0),
    ]
    
    for i, vp in enumerate(test_viewports):
        assignments = adapter.assign_quality(vp)
        bandwidth = adapter.calculate_bandwidth(assignments)
        print(f"   Viewport {i+1} (yaw={vp.yaw}°, pitch={vp.pitch}°):")
        print(f"     - VP: {len(assignments['VP'])}, VN: {len(assignments['VN'])}, VZ: {len(assignments['VZ'])}")
        print(f"     - Bandwidth: {bandwidth['total_bitrate_mbps']:.1f} Mbps, Savings: {bandwidth['bandwidth_savings_percent']:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ Tile adaptation test passed!")
    print("=" * 60)


if __name__ == '__main__':
    test_tile_adaptation()

