<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet
    version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs">

    <xsl:output method="text" />

    <xsl:variable name="separator" select="'&#59;'" />
    <xsl:variable name="newline" select="'&#10;'" />

    <xsl:template match="/">
        <xsl:text>Index Term;Count</xsl:text>
        <xsl:value-of select="$newline" />
        <xsl:for-each select="//fanfiction/index_terms/index_term">
        <xsl:sort select="text()" data-type="text" />
            <xsl:value-of select="text()"/>
            <xsl:value-of select="$newline" />
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>