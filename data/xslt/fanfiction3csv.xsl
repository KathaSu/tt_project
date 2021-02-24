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
        <xsl:for-each-group select="//fanfiction" group-by="index_terms/index_term/text()">
            <xsl:sort select="count(current-group()/title)" data-type="number">
            <xsl:value-of select="current-grouping-key()"/>
            <xsl:value-of select="$separator" />
            <xsl:value-of select="count(current-group()/title)"/>
            <xsl:value-of select="$newline" />
        </xsl:for-each-group>
    </xsl:template>
</xsl:stylesheet>