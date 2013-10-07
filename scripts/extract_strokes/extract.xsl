<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:svg="http://www.w3.org/2000/svg">
<xsl:output       
	method="xml"
    indent="yes"
    standalone="no"
    doctype-public="-//W3C//DTD SVG 1.1//EN"
    doctype-system="http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
    media-type="image/svg"/>

<!-- FILTERS -->

<xsl:template match="svg:path">
<xsl:if test="substring-after(@id,'-s') &lt; MAX and substring-after(@id,'-s') &gt; MIN">
<xsl:copy-of select="."/>
</xsl:if>
</xsl:template>

<!-- skip g element with text element as children -->
<xsl:template match="svg:g[svg:text]">
</xsl:template>


<!-- IDENTITY TRANFROMATION -->
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>




</xsl:stylesheet>
