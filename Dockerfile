FROM squidfunk/mkdocs-material

RUN pip install --no-cache-dir \
	mkdocs-awesome-pages-plugin==2.9.2 \
	mkdocs-video mkdocs-redirects==1.2.1 \
	mkdocs-material==9.5.1 \
	mkdocs-video==1.5.0

ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
