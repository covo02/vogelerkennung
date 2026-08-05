### Reset button in the header row (left side, next to CSV export)

Callback that:

- Rebuilds the live figure from scratch.

- Restores camera positions from camera_positions_enu.

- Restores event points from processed_events_by_id.

- Returns a fresh figure with uirevision="keep-view" to preserve camera view.

- Clears camera_positions_enu - removes all cached camera ENU positions.

- Sets gps_reference_point = None - allows pi1 to be re-determined from the next event.

