# Thin entry point that delegates to brand/Makefile.
# Run `make help` here, or `make -C brand <target>` directly.

.SILENT:
.ONESHELL:
.DEFAULT_GOAL := help
.PHONY: help brand brand_paths brand_avatar brand_wordmark brand_social brand_clean setup_brand_fonts

help brand brand_paths brand_avatar brand_wordmark brand_social brand_clean setup_brand_fonts:
	$(MAKE) --no-print-directory -C brand $@
