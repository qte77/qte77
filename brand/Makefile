# Brand asset generation. Run from inside brand/ (or `make -C brand <target>`).
# Uses `uv` for Python dependencies. Run `make help` to see all recipes.

.SILENT:
.ONESHELL:
.PHONY: \
	setup_brand_fonts \
	brand brand_paths brand_avatar brand_social brand_clean \
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


brand:  ## Refresh all brand artifacts (fonts + avatar + social previews)
	$(MAKE) -s setup_brand_fonts
	$(MAKE) -s brand_avatar
	$(MAKE) -s brand_social

brand_paths:  ## Convert canonical $(IMAGES)/logo-mark.svg -> $(IMAGES)/logo-mark.paths.svg (path-only, for inspection)
	echo "Converting text -> paths ..."
	uv run $(SCRIPTS)/svg_text_to_paths.py \
		--font $(FONTS)/JetBrainsMono-Bold.ttf \
		< $(IMAGES)/logo-mark.svg \
		> $(IMAGES)/logo-mark.paths.svg
	echo "wrote $(IMAGES)/logo-mark.paths.svg"

brand_avatar:  ## Rasterize $(IMAGES)/logo-mark.svg -> $(IMAGES)/avatar_{dark,light}.png (920x920). Flag: ONLY=dark|light
	echo "Rendering avatar ..."
	uv run $(SCRIPTS)/render_avatar.py $(if $(ONLY),--only $(ONLY))

brand_social:  ## Generate $(DIST)/<repo>-social.png from social-previews.toml. Flags: ONLY=<repo>, LIGHT=1, DARK=1
	echo "Rendering social preview cards ..."
	uv run $(SCRIPTS)/generate_social.py \
		$(if $(ONLY),--only $(ONLY)) \
		$(if $(filter 1,$(LIGHT)),--light) \
		$(if $(filter 1,$(DARK)),--dark)

brand_clean:  ## Remove $(DIST)/, derived path SVG, and downloaded fonts
	echo "Cleaning brand artifacts ..."
	rm -rf $(DIST)
	rm -f $(IMAGES)/logo-mark.paths.svg
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
