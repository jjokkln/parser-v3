from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os

class ProfileGenerator:
    """Klasse zur Erstellung von PDF-Profilen aus strukturierten Daten"""
    
    def __init__(self):
        """Initialisiert den Profil-Generator mit Stilen"""
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
    
    def generate_profile(self, profile_data, output_path, template="professional"):
        """
        Generiert ein PDF-Profil aus den extrahierten Daten
        
        Args:
            profile_data: Dictionary mit Profildaten
            output_path: Pfad für die Ausgabedatei
            template: Art der Vorlage (professional, classic, modern, minimalist)
        
        Returns:
            Pfad zur generierten PDF-Datei
        """
        # Erstelle das PDF-Dokument
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20*mm, 
            leftMargin=20*mm,
            topMargin=20*mm, 
            bottomMargin=20*mm
        )
        
        # Erstelle die Dokumentelemente basierend auf der gewählten Vorlage
        elements = self._create_document_elements(profile_data, template)
        
        # Erstelle das PDF
        doc.build(elements)
        
        return output_path
    
    def _create_custom_styles(self):
        """Erstellt benutzerdefinierte Stile für das Dokument"""
        custom_styles = {}
        
        # GALDORA Überschrift-Stil (große schwarze Schrift)
        custom_styles['GaldoraLogo'] = ParagraphStyle(
            'GaldoraLogo',
            parent=self.styles['Normal'],
            fontSize=36,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=0.1*cm
        )

        # Tagline unter dem Logo
        custom_styles['Tagline'] = ParagraphStyle(
            'Tagline',
            parent=self.styles['Italic'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            textColor=colors.black,
            spaceAfter=1.5*cm
        )
        
        # Profil Überschrift
        custom_styles['ProfilTitle'] = ParagraphStyle(
            'ProfilTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1973B8'),  # GALDORA Blau
            spaceBefore=0.5*cm,
            spaceAfter=0.2*cm
        )
        
        # Name
        custom_styles['Name'] = ParagraphStyle(
            'Name',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica',
            spaceBefore=0.2*cm,
            spaceAfter=1.5*cm
        )
        
        # Überschrift für Abschnitte (Beruflicher Werdegang, Ausbildung, etc.)
        custom_styles['Heading2'] = ParagraphStyle(
            'Heading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceBefore=1.0*cm,
            spaceAfter=0.3*cm,
            underline=1  # Unterstreichung
        )
        
        # Ansprechpartner Überschrift
        custom_styles['ContactHeader'] = ParagraphStyle(
            'ContactHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceBefore=0.2*cm,
            spaceAfter=0.1*cm
        )
        
        # Normaler Text
        custom_styles['Normal'] = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=0.2*cm
        )
        
        # Label-Text (fett)
        custom_styles['Label'] = ParagraphStyle(
            'Label',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=0.1*cm
        )
        
        # Firmenname - Hervorgehoben
        custom_styles['Company'] = ParagraphStyle(
            'Company',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=0.1*cm
        )
        
        # Position/Rolle - Kursiv
        custom_styles['Position'] = ParagraphStyle(
            'Position',
            parent=self.styles['Italic'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            spaceAfter=0.2*cm
        )
        
        # Zeitraum - Linksbündig für erste Spalte 
        custom_styles['Period'] = ParagraphStyle(
            'Period',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            alignment=0,  # Linksbündig
            spaceAfter=0.1*cm
        )
        
        # Aufgabenpunkt - für rechte Spalte
        custom_styles['TaskPoint'] = ParagraphStyle(
            'TaskPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=0,  # Linksbündig
            leftIndent=0.5*cm,
            bulletIndent=0.3*cm,
            spaceAfter=0.1*cm
        )
        
        # GALDORA Fußzeile
        custom_styles['Footer'] = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            alignment=1,  # Zentriert
            spaceBefore=0.2*cm,
            textColor=colors.black
        )
        
        return custom_styles
    
    def _create_document_elements(self, profile_data, template="professional"):
        """
        Erstellt die Elemente für das PDF-Dokument basierend auf dem Design der Profilvorlage
        
        Args:
            profile_data: Dictionary mit Profildaten
            template: Art der Vorlage (professional, classic, modern, minimalist)
        
        Returns:
            Liste mit PDF-Elementen
        """
        elements = []
        
        # Korrekte Pfade zum Verzeichnis der Quellendateien
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sources_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'sources')
        
        # Wenn sources nicht existiert, versuche relative Pfade vom Arbeitsverzeichnis
        if not os.path.exists(sources_dir):
            sources_dir = 'sources'
        
        # GALDORA Logo aus dem sources-Ordner einbinden
        logo_path = os.path.join(sources_dir, 'galdoralogo.png')
        
        # Erstelle eine Tabelle für das Logo links oben (nicht gestreckt)
        if os.path.exists(logo_path):
            # Logo-Größe korrigieren (Original-Proportionen beibehalten)
            img = Image(logo_path, width=120, height=20)  # Korrigierte Größe mit besseren Proportionen
            # Logo-Tabelle für korrektes Alignment links
            logo_table = Table([[img]], colWidths=[400])
            logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(logo_table)
            
            # Tagline in eigener Tabelle für korrekte Ausrichtung
            tagline_table = Table([[Paragraph("Ich bin, was wir tun", self.custom_styles['Tagline'])]], colWidths=[400])
            tagline_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(tagline_table)
        else:
            # Fallback wenn Bild nicht gefunden wurde
            elements.append(Paragraph("GALDORA", self.custom_styles['GaldoraLogo']))
            elements.append(Paragraph("Ich bin, was wir tun", self.custom_styles['Tagline']))
        
        # Profil Überschrift
        elements.append(Paragraph("Profil", self.custom_styles['ProfilTitle']))
        
        # Persönliche Daten
        personal_data = profile_data.get('persönliche_daten', {})
        
        # Name
        name = personal_data.get('name', 'Profil')
        elements.append(Paragraph(name, self.custom_styles['Name']))
        
        # Ansprechpartner Block mit IHR ANSPRECHPARTNER und den entsprechenden Informationen
        elements.append(Paragraph("IHR ANSPRECHPARTNER", self.custom_styles['ContactHeader']))
        
        # Kontaktinformationen
        kontakt = personal_data.get('kontakt', {})
        ansprechpartner = kontakt.get('ansprechpartner', '')
        nachname = ansprechpartner.split()[-1] if ansprechpartner else 'Fischer'
        anrede = f"Herr {nachname}"
        telefon = kontakt.get('telefon', '02161 62126-02')
        email = kontakt.get('email', f"{nachname.lower()}@galdora.de")
            
        # Erstelle Layout für Ansprechpartner
        elements.append(Paragraph(anrede, self.custom_styles['Normal']))
        elements.append(Paragraph(f"Telefon: {telefon}", self.custom_styles['Normal']))
        elements.append(Paragraph(f"E-Mail: {email}", self.custom_styles['Normal']))
        
        # Horizontale Linie nach Ansprechpartner mit etwas Abstand
        elements.append(Spacer(1, 0.8*cm))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey))
        elements.append(Spacer(1, 0.2*cm))
        
        # Persönliche Informationen (aus Profilvorlage Seite 1)
        elements.append(Paragraph("Wohnort:", self.custom_styles['Label']))
        elements.append(Paragraph(personal_data.get('wohnort', ''), self.custom_styles['Normal']))
        
        elements.append(Paragraph("Jahrgang:", self.custom_styles['Label']))
        elements.append(Paragraph(personal_data.get('jahrgang', ''), self.custom_styles['Normal']))
        
        elements.append(Paragraph("Führerschein:", self.custom_styles['Label']))
        elements.append(Paragraph(personal_data.get('führerschein', ''), self.custom_styles['Normal']))
        
        # Wunschgehalt (wenn vorhanden)
        wunschgehalt = profile_data.get('wunschgehalt', '')
        if wunschgehalt:
            elements.append(Paragraph("Gehalt:", self.custom_styles['Label']))
            elements.append(Paragraph(wunschgehalt, self.custom_styles['Normal']))
        
        # Beruflicher Werdegang
        elements.append(Paragraph("Beruflicher Werdegang", self.custom_styles['Heading2']))
        
        # Berufserfahrung mit 2-spaltigem Layout (Daten links, Aufgaben rechts)
        berufserfahrung = profile_data.get('berufserfahrung', [])
        for erfahrung in berufserfahrung:
            # Zeitraum
            zeitraum = erfahrung.get('zeitraum', '')
            unternehmen = erfahrung.get('unternehmen', '')
            position = erfahrung.get('position', '')
            
            # Aufgaben vorbereiten und auf max. 4 (idealerweise 3) begrenzen
            aufgaben = erfahrung.get('aufgaben', [])
            aufgaben_formatted = []
            
            # Wenn zu viele Aufgaben, reduziere auf 3 zusammengefasste Punkte
            if len(aufgaben) > 4:
                # Wir teilen die Aufgaben in drei Gruppen und fassen jede zusammen
                chunks = [aufgaben[i:i + len(aufgaben)//3 + (1 if i < len(aufgaben) % 3 else 0)] 
                          for i in range(0, len(aufgaben), len(aufgaben)//3 + (1 if 0 < len(aufgaben) % 3 else 0))]
                
                for chunk in chunks[:3]:  # Maximal 3 zusammengefasste Punkte
                    combined = "; ".join(chunk)
                    aufgaben_formatted.append(Paragraph(f"• {combined}", self.custom_styles['Normal']))
            else:
                # Wenn 4 oder weniger Aufgaben, behalte sie einzeln bei
                for i, aufgabe in enumerate(aufgaben[:4]):  # Maximal 4 Aufgaben
                    aufgaben_formatted.append(Paragraph(f"• {aufgabe}", self.custom_styles['Normal']))
            
            # Linke Spalte mit Zeitraum, Unternehmen und Position
            left_column = [
                Paragraph(zeitraum, self.custom_styles['Period']),
                Paragraph(unternehmen, self.custom_styles['Company']),
                Paragraph(position, self.custom_styles['Position'])
            ]
            
            # Rechte Spalte mit Aufgaben
            right_column = aufgaben_formatted
            
            # Ausgleich für den Fall, dass eine Spalte mehr Zeilen hat als die andere
            max_rows = max(len(left_column), len(right_column))
            
            while len(left_column) < max_rows:
                left_column.append(Paragraph("", self.custom_styles['Normal']))
            
            while len(right_column) < max_rows:
                right_column.append(Paragraph("", self.custom_styles['Normal']))
            
            # Erstelle die Tabelle mit den zwei Spalten
            data = []
            for i in range(max_rows):
                data.append([left_column[i], right_column[i]])
            
            # Tabelle mit definierter Breite (30% links, 70% rechts)
            col_widths = [A4[0] * 0.25, A4[0] * 0.55]  # Ungefähr 30% und 70% der Seitenbreite
            
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.3*cm))
        
        # Zweite Seite für Ausbildung/Weiterbildung
        elements.append(PageBreak())
        
        # Logo auf der zweiten Seite wiederholen
        if os.path.exists(logo_path):
            # Logo-Größe korrigieren (Original-Proportionen beibehalten)
            img = Image(logo_path, width=120, height=20)  # Korrigierte Größe mit besseren Proportionen
            # Logo-Tabelle für korrektes Alignment links
            logo_table = Table([[img]], colWidths=[400])
            logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(logo_table)
            
            # Tagline in eigener Tabelle für korrekte Ausrichtung
            tagline_table = Table([[Paragraph("Ich bin, was wir tun", self.custom_styles['Tagline'])]], colWidths=[400])
            tagline_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(tagline_table)
        
        # Ausbildung
        elements.append(Paragraph("Ausbildung/ Weiterbildung", self.custom_styles['Heading2']))
        
        # Ausbildungen
        ausbildungen = profile_data.get('ausbildung', [])
        for ausbildung in ausbildungen:
            # Zeitraum
            zeitraum = ausbildung.get('zeitraum', '')
            elements.append(Paragraph(zeitraum, self.custom_styles['Period']))
            
            # Institution und Abschluss
            institution = ausbildung.get('institution', '')
            abschluss = ausbildung.get('abschluss', '')
            elements.append(Paragraph(f"Studium {institution}", self.custom_styles['Company']))
            
            # Studienschwerpunkte
            schwerpunkte = ausbildung.get('schwerpunkte', '')
            if schwerpunkte:
                elements.append(Paragraph(f"Studienschwerpunkte: {schwerpunkte}", self.custom_styles['Normal']))
            
            # Abschluss
            if abschluss:
                elements.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
            
            # Note 
            note = ausbildung.get('note', '')
            if note:
                elements.append(Paragraph(f"Abschlussnote {note}", self.custom_styles['Normal']))
            
            # Abstand
            elements.append(Spacer(1, 0.3*cm))
        
        # Weiterbildungen
        weiterbildungen = profile_data.get('weiterbildungen', [])
        for weiterbildung in weiterbildungen:
            # Zeitraum
            zeitraum = weiterbildung.get('zeitraum', '')
            elements.append(Paragraph(zeitraum, self.custom_styles['Period']))
            
            # Bezeichnung und Abschluss
            bezeichnung = weiterbildung.get('bezeichnung', '')
            abschluss = weiterbildung.get('abschluss', '')
            
            if "Fortbildung" in bezeichnung:
                elements.append(Paragraph(bezeichnung, self.custom_styles['Company']))
            else:
                elements.append(Paragraph(f"Fortbildung {bezeichnung}", self.custom_styles['Company']))
            
            # Abschluss
            if abschluss:
                elements.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
            
            # Abstand
            elements.append(Spacer(1, 0.3*cm))
        
        # Footer mit GALDORA Kontaktinformationen
        elements.append(Spacer(1, 1.0*cm))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=0.5*cm))
        elements.append(Spacer(1, 0.2*cm))
        
        footer_text = "GALDORA Personalmanagement GmbH Co.KG\nVolksgartenstr. 85-89, 41065 Mönchengladbach\nE-Mail: info@galdora.de / Web: www.galdora.de"
        elements.append(Paragraph(footer_text, self.custom_styles['Footer']))
        
        return elements


def check_missing_profile_data(profile_data):
    """
    Überprüft, ob wichtige Daten im Profil fehlen
    
    Args:
        profile_data: Dictionary mit Profildaten
    
    Returns:
        Liste mit fehlenden Datenfeldern
    """
    missing_data = []
    
    # Persönliche Daten prüfen
    personal_data = profile_data.get('persönliche_daten', {})
    if not personal_data.get('name'):
        missing_data.append('Name')
    
    # Kontaktdaten prüfen
    kontakt = personal_data.get('kontakt', {})
    if not kontakt.get('email') and not kontakt.get('telefon'):
        missing_data.append('Kontaktdaten (E-Mail oder Telefon)')
    
    # Wohnort prüfen
    if not personal_data.get('wohnort'):
        missing_data.append('Wohnort')
    
    # Jahrgang prüfen
    if not personal_data.get('jahrgang'):
        missing_data.append('Jahrgang')
    
    # Berufserfahrung prüfen
    berufserfahrung = profile_data.get('berufserfahrung', [])
    if not berufserfahrung:
        missing_data.append('Berufserfahrung')
    
    # Ausbildung prüfen
    ausbildung = profile_data.get('ausbildung', [])
    if not ausbildung:
        missing_data.append('Ausbildung')
    
    return missing_data
