<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet
    version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs">

    
    <xsl:template match="/">
    <html>
        <body>
            <h2>Fanfiction Collection</h2>
            <table border="1">
                <tr bgcolor="#9acd32">
                    <th>Term</th>
                    <th>Count</th>
                </tr>
                <xsl:for-each-group select="//fanfiction[age_rating/text()='mature']" group-by="index_terms/index_term/text()">
                    <xsl:sort select="count(current-group()/title)" data-type="number" order="descending"/>
                    <tr>
                    <td><xsl:value-of select="current-grouping-key()"/></td>
                    <td><xsl:value-of select="count(current-group()/title)"/></td>
                    </tr>
                </xsl:for-each-group>
            </table>
        </body>
    </html>
    </xsl:template>

</xsl:stylesheet>