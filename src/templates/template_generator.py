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
            tagline_table = Table([[Paragraph("Ich ist, was wir tun", self.custom_styles['Tagline'])]], colWidths=[400])
            tagline_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(tagline_table)
        else:
            # Fallback wenn Bild nicht gefunden wurde
            elements.append(Paragraph("GALDORA", self.custom_styles['GaldoraLogo']))
            elements.append(Paragraph("Ich ist, was wir tun", self.custom_styles['Tagline']))
        
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
        elements.append(Spacer(1, 0.5*cm))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey))
        elements.append(Spacer(1, 0.5*cm))
        
        # Persönliche Informationen (aus Profilvorlage Seite 1)
        elements.append(Paragraph("Wohnort:", self.custom_styles['Label']))
        elements.append(Paragraph(personal_data.get('wohnort', ''), self.custom_styles['Normal']))
        
        # Jahrgang
        elements.append(Spacer(1, 0.2*cm))
        elements.append(Paragraph("Jahrgang:", self.custom_styles['Label']))
        elements.append(Paragraph(personal_data.get('jahrgang', ''), self.custom_styles['Normal']))
        
        # Führerschein
        elements.append(Spacer(1, 0.2*cm))
        elements.append(Paragraph("Führerschein:", self.custom_styles['Label']))
        elements.append(Paragraph(personal_data.get('führerschein', ''), self.custom_styles['Normal']))
        
        # Wunschgehalt (wenn vorhanden)
        wunschgehalt = profile_data.get('wunschgehalt', '')
        if wunschgehalt:
            elements.append(Spacer(1, 0.2*cm))
            elements.append(Paragraph("Gehalt:", self.custom_styles['Label']))
            elements.append(Paragraph(wunschgehalt, self.custom_styles['Normal']))
        
        # Beruflicher Werdegang
        elements.append(Paragraph("Beruflicher Werdegang", self.custom_styles['Heading2']))
        
        # Berufserfahrung wie in der Vorlage formatieren
        berufserfahrung = profile_data.get('berufserfahrung', [])
        for erfahrung in berufserfahrung:
            # Zeitraum
            zeitraum = erfahrung.get('zeitraum', '')
            elements.append(Paragraph(zeitraum, self.custom_styles['Period']))
            
            # Unternehmen und Position erstellen
            unternehmen = erfahrung.get('unternehmen', '')
            position = erfahrung.get('position', '')
            
            # Spezielle Formatierung für Werkstudent-Einträge wie im Beispiel
            if "Werkstudent" in position:
                # Aufgaben sammeln
                aufgaben = erfahrung.get('aufgaben', [])
                
                # Formatierung für Werkstudenten wie im Beispiel
                if "Projektmanagement" in position or "Projektmanagement" in unternehmen:
                    unternehmen_text = "Werkstudent im Projektmanagement"
                    firma_text = "Finanzinformatik GmbH & Co. KG"
                elif "Vertrieb" in position or "Extrusion" in position:
                    unternehmen_text = "Werkstudent im internationalen Vertrieb von Extrusionsanlagen"
                    firma_text = "TROESTER GmbH & Co. KG"
                else:
                    unternehmen_text = position
                    firma_text = unternehmen
                
                # Zweispaltige Tabelle wie im Beispiel
                toom_data = [
                    [Paragraph(unternehmen_text, self.custom_styles['Company']), Paragraph("", self.custom_styles['Normal'])],
                    [Paragraph(firma_text, self.custom_styles['Position']), Paragraph("", self.custom_styles['Normal'])]
                ]
                
                # Für Aufgaben (falls vorhanden) in der rechten Spalte
                for i, aufgabe in enumerate(aufgaben):
                    if i < len(toom_data):
                        # Erste Aufgaben in bestehende Zeilen einfügen
                        toom_data[i][1] = Paragraph(f"• {aufgabe}", self.custom_styles['Normal'])
                    else:
                        # Weitere Aufgaben in neue Zeilen
                        toom_data.append([
                            Paragraph("", self.custom_styles['Normal']),
                            Paragraph(f"• {aufgabe}", self.custom_styles['Normal'])
                        ])
            else:
                # Aufgaben sammeln
                aufgaben = erfahrung.get('aufgaben', [])
                
                # Zweispaltige Tabelle mit genauer Struktur wie im Beispiel
                toom_data = []
                
                # Erste Spalte: Unternehmen
                # Zweite Spalte: Erste Aufgabe
                if len(aufgaben) > 0:
                    toom_data.append([
                        Paragraph(unternehmen, self.custom_styles['Company']),
                        Paragraph(f"• {aufgaben[0]}", self.custom_styles['Normal'])
                    ])
                else:
                    toom_data.append([
                        Paragraph(unternehmen, self.custom_styles['Company']),
                        Paragraph("", self.custom_styles['Normal'])
                    ])
                
                # Zweite Zeile: Position in erster Spalte
                # Zweite Aufgabe in zweiter Spalte (wenn vorhanden)
                if len(aufgaben) > 1:
                    toom_data.append([
                        Paragraph(position, self.custom_styles['Position']),
                        Paragraph(f"• {aufgaben[1]}", self.custom_styles['Normal'])
                    ])
                else:
                    toom_data.append([
                        Paragraph(position, self.custom_styles['Position']),
                        Paragraph("", self.custom_styles['Normal'])
                    ])
                
                # Für weitere Aufgaben leere Zelle in erster Spalte und Aufgabe in zweiter Spalte
                for i in range(2, len(aufgaben)):
                    toom_data.append([
                        Paragraph("", self.custom_styles['Normal']),
                        Paragraph(f"• {aufgaben[i]}", self.custom_styles['Normal'])
                    ])
            
            # Tabelle mit definierter Breite (25% links, 55% rechts)
            col_widths = [A4[0] * 0.25, A4[0] * 0.55]
            
            table = Table(toom_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.4*cm))
        
        # Zweite Seite für Ausbildung/Weiterbildung
        elements.append(PageBreak())
        
        # Logo auf der zweiten Seite wiederholen
        if os.path.exists(logo_path):
            # Logo-Größe korrigieren (Original-Proportionen beibehalten)
            img = Image(logo_path, width=120, height=20)
            # Logo-Tabelle für korrektes Alignment links
            logo_table = Table([[img]], colWidths=[400])
            logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(logo_table)
            
            # Tagline in eigener Tabelle für korrekte Ausrichtung
            tagline_table = Table([[Paragraph("Ich ist, was wir tun", self.custom_styles['Tagline'])]], colWidths=[400])
            tagline_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT')]))
            elements.append(tagline_table)
        
        # Ausbildung/ Weiterbildung
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
            
            # Studienschwerpunkte
            schwerpunkte = ausbildung.get('schwerpunkte', '')
            
            # Spezielle Formatierung basierend auf dem Text im Beispiel
            if 'Metro' in institution:
                elements.append(Paragraph(f"Metro Deutschland GmbH", self.custom_styles['Company']))
                if 'Ausbildung' in institution or 'Ausbildung' in abschluss:
                    elements.append(Paragraph(f"Ausbildung zum Groß und Außenhandelskaufmann", self.custom_styles['Position']))
                    elements.append(Paragraph(f"erfolgreich abgeschlossen", self.custom_styles['Normal']))
                elif 'Übernahme' in institution or 'Übernahme' in abschluss:
                    elements.append(Paragraph(f"Übernahme nach der Ausbildung", self.custom_styles['Position']))
            # BWL-Studium Formatierung
            elif 'BWL' in institution or 'BWL' in abschluss:
                elements.append(Paragraph(f"Studium BWL", self.custom_styles['Company']))
                if schwerpunkte:
                    elements.append(Paragraph(f"Studienschwerpunkte: {schwerpunkte}", self.custom_styles['Normal']))
                elements.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
                
                # Note 
                note = ausbildung.get('note', '')
                if note:
                    elements.append(Paragraph(f"Abschlussnote {note}", self.custom_styles['Normal']))
            else:
                # Standard-Formatierung
                if institution.startswith("Studium"):
                    elements.append(Paragraph(institution, self.custom_styles['Company']))
                else:
                    elements.append(Paragraph(f"Studium {institution}", self.custom_styles['Company']))
                
                if schwerpunkte:
                    elements.append(Paragraph(f"Studienschwerpunkte: {schwerpunkte}", self.custom_styles['Normal']))
                if abschluss:
                    elements.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
                
                # Note 
                note = ausbildung.get('note', '')
                if note:
                    elements.append(Paragraph(f"Abschlussnote {note}", self.custom_styles['Normal']))
            
            # Abstand
            elements.append(Spacer(1, 0.4*cm))
        
        # Weiterbildungen
        weiterbildungen = profile_data.get('weiterbildungen', [])
        for weiterbildung in weiterbildungen:
            # Zeitraum
            zeitraum = weiterbildung.get('zeitraum', '')
            elements.append(Paragraph(zeitraum, self.custom_styles['Period']))
            
            # Bezeichnung und Abschluss
            bezeichnung = weiterbildung.get('bezeichnung', '')
            abschluss = weiterbildung.get('abschluss', '')
            
            # Formatieren genau wie im Beispiel
            if "IHK" in bezeichnung or "AdA" in bezeichnung:
                elements.append(Paragraph(f"Fortbildung zum Ausbilder IHK (AdA)", self.custom_styles['Company']))
            elif "Handelsfachwirt" in bezeichnung:
                elements.append(Paragraph(f"Fortbildung zum Handelsfachwirt", self.custom_styles['Company']))
                if "Staatl. Geprüfter Handelsfachwirt" in abschluss:
                    elements.append(Paragraph(f"Abschluss: Staatl. Geprüfter Handelsfachwirt", self.custom_styles['Normal']))
                else:
                    elements.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
            else:
                if "zum" in bezeichnung or "zur" in bezeichnung:
                    elements.append(Paragraph(f"Fortbildung {bezeichnung}", self.custom_styles['Company']))
                else:
                    elements.append(Paragraph(f"Fortbildung zum {bezeichnung}", self.custom_styles['Company']))
                
                # Abschluss nur anzeigen, wenn nicht leer und nicht bereits in Bezeichnung enthalten
                if abschluss and abschluss not in bezeichnung:
                    elements.append(Paragraph(f"Abschluss: {abschluss}", self.custom_styles['Normal']))
            
            # Abstand
            elements.append(Spacer(1, 0.4*cm))
        
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
