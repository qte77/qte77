# Brand asset generation. Run from inside brand/ (or `make -C brand <target>`).
# Uses `uv` for Python dependencies. Run `make help` to see all recipes.

.SILENT:
.ONESHELL:
.PHONY: \
	setup_brand_fonts \
	brand brand_paths brand_avatar brand_wordmark brand_social brand_clean \
	help
.DEFAULT_GOAL := help


# -- paths --
IMAGES   := images
FONTS    := fonts
DIST     := dist
SCRIPTS  := scripts


# MARK: SETUP


setup_brand_fonts:  ## Download Inter + JetBrains Mono (OFL) into brand/fonts/
	echo "Installing brand fonts ..."
	uv run $(SCRIPTS)/install_fonts.py


# MARK: BRAND


brand:  ## Refresh all brand artifacts (fonts + paths + avatar + wordmark + social)
	$(MAKE) -s setup_brand_fonts
	$(MAKE) -s brand_paths
	$(MAKE) -s brand_avatar
	$(MAKE) -s brand_wordmark
	$(MAKE) -s brand_social

brand_paths:  ## Convert canonical SVGs -> $(IMAGES)/{logo-mark,logo-wordmark}.paths.svg (font geometry baked in)
	echo "Converting text -> paths ..."
	for src in logo-mark logo-wordmark; do \
		uv run $(SCRIPTS)/svg_text_to_paths.py \
			--font $(FONTS)/JetBrainsMono-Bold.ttf \
			< $(IMAGES)/$$src.svg \
			> $(IMAGES)/$$src.paths.svg; \
		echo "wrote $(IMAGES)/$$src.paths.svg"; \
	done

brand_avatar:  ## Rasterize $(IMAGES)/logo-mark.svg -> $(IMAGES)/avatar_{dark,light}.png (920x920). Flag: ONLY=dark|light
	echo "Rendering avatar ..."
	uv run $(SCRIPTS)/render_avatar.py $(if $(ONLY),--only $(ONLY))

brand_wordmark:  ## Rasterize $(IMAGES)/logo-wordmark.svg -> $(IMAGES)/wordmark_{dark,light}.png (960x320). Flag: ONLY=dark|light
	echo "Rendering wordmark ..."
	uv run $(SCRIPTS)/render_wordmark.py $(if $(ONLY),--only $(ONLY))

brand_social:  ## Generate $(DIST)/<repo>-social.png from social-previews.toml. Flags: ONLY=<repo>, LIGHT=1, DARK=1
	echo "Rendering social preview cards ..."
	uv run $(SCRIPTS)/generate_social.py \
		$(if $(ONLY),--only $(ONLY)) \
		$(if $(filter 1,$(LIGHT)),--light) \
		$(if $(filter 1,$(DARK)),--dark)

brand_clean:  ## Remove $(DIST)/ and downloaded fonts (paths SVGs and PNGs are committed artifacts)
	echo "Cleaning brand artifacts ..."
	rm -rf $(DIST)
	rm -f $(FONTS)/*.ttf $(FONTS)/*.otf


# MARK: HELP


help:  ## Show available recipes grouped by section
	@echo "Usage: make [recipe]"
	@echo ""
	@awk \
		-v IMAGES="$(IMAGES)" -v FONTS="$(FONTS)" \
		-v DIST="$(DIST)" -v SCRIPTS="$(SCRIPTS)" \
	'/^# MARK:/ { \
		section = substr($$0, index($$0, ":")+2); \
		printf "\n\033[1m%s\033[0m\n", section \
	} \
	/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			recipe = $$1; \
			sub(/:/, "", recipe); \
			msg = substr($$0, RSTART + 3, RLENGTH); \
			gsub(/\$$\(IMAGES\)/,  IMAGES,  msg); \
			gsub(/\$$\(FONTS\)/,   FONTS,   msg); \
			gsub(/\$$\(DIST\)/,    DIST,    msg); \
			gsub(/\$$\(SCRIPTS\)/, SCRIPTS, msg); \
			printf "  \033[36m%-22s\033[0m %s\n", recipe, msg \
		} \
	}' $(MAKEFILE_LIST)
