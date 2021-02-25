<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text" />

<xsl:variable name="separator" select="'&#59;'" />
<xsl:variable name="newline" select="'&#10;'" />

<xsl:template match="/">
<xsl:text>ID, Title,Author,Authortags,Characters,Index Terms</xsl:text>
<xsl:value-of select="$newline" />
<xsl:for-each select="//fanfiction">
<xsl:sort select="title"/>
<xsl:if test="index_terms/index_term/text() = 'perfume'">
<xsl:value-of select="@id"/>
<xsl:value-of select="$separator" />
<xsl:value-of select="title"/>
<xsl:value-of select="$separator" />
<xsl:value-of select="author" />
<xsl:value-of select="$separator" />
<xsl:for-each select="authortags/authortag"><xsl:value-of select="text()"/>, </xsl:for-each>
<xsl:value-of select="$separator" />
<xsl:for-each select="characters/character"><xsl:value-of select="text()"/>, </xsl:for-each>
<xsl:value-of select="$separator" />
<xsl:for-each select="index_terms/index_term"><xsl:value-of select="text()"/>, </xsl:for-each>
<xsl:value-of select="$newline" />
</xsl:if>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>