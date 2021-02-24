<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
<html>
    <body>
        <h2>Fanfiction Collection</h2>
        <table border="1">
            <tr bgcolor="#9acd32">
                <th>Title</th>
                <th>Author</th>
                <th>Authortags</th>
                <th>Characters</th>
                <th>Index Terms</th>
            </tr>
            <xsl:for-each select="fanfiction_database/fanfictions/fanfiction">
            <xsl:sort select="title"/>
            <tr>
                <td>
                    <xsl:value-of select="title"/>
                </td>
                <td>
                    <xsl:value-of select="author"/></td>
                <td>
                    <xsl:for-each select="authortags/authortag">
                        <xsl:value-of select="text()"/><br/>
                    </xsl:for-each>
                </td>
                <td>
                    <xsl:for-each select="characters/character">
                        <xsl:value-of select="text()"/><br/>
                    </xsl:for-each>
                </td>
                <td>
                    <xsl:for-each select="index_terms/index_term">
                        <xsl:choose>
                            <xsl:when test="text() = 'potion'">
                                <b><xsl:value-of select="text()"/></b><br/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="text()"/><br/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </td>
            </tr>
            </xsl:for-each>
        </table>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>