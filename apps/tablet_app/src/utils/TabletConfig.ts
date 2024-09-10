/*
 * Copyright (C) 2024. Archimedes Exhibitions GmbH,
 * Saarbrücker Str. 24, Berlin, Germany
 *
 * This file contains proprietary source code and confidential
 * information. Its contents may not be disclosed or distributed to
 * third parties unless prior specific permission by Archimedes
 * Exhibitions GmbH, Berlin, Germany is obtained in writing. This applies
 * to copies made in any form and using any medium. It applies to
 * partial as well as complete copies.
 */

class TabletConfig {
  public data: any | undefined = undefined

  get timeColor() {
    return this.data.graph_view.time_color
  }

  get costColor() {
    return this.data.graph_view.cost_color
  }

  get efficiencyColor() {
    return this.data.graph_view.efficiency_color
  }

  get qrScanDelay() {
    return this.data.scan_view.scan_delay
  }

  get backendPath() {
    return this.data.api_path
  }

  get showFullscreenPrompt() {
    return this.data.show_fullscreen_prompt
  }

  get disableRightClick() {
    return this.data.disable_right_click
  }

  get maxTeamNameLength() {
    return this.data.team_name_view.max_team_name
  }

  get lottieWasmUrl() {
    return this.data.dotlottie.wasmUrl
  }

  constructor() {}
}

export const tabletConfig = new TabletConfig()
