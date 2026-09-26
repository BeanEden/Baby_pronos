with open('templates/admin_info.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []

for i, line in enumerate(lines):
    if '<!-- Sauvegarde & Restauration -->' in line:
        new_lines.append('<details class="accordion">\n')
        new_lines.append('<summary>💾 Sauvegarde & Restauration</summary>\n')
        new_lines.append('<div class="accordion-content">\n')
    
    if '<h3 style="margin-top: 0; color: #6c5ce7; display: flex; align-items: center; gap: 8px;">💾 Sauvegarde & Restauration</h3>' in line:
        continue # skip
        
    if '<h3>Informations générales</h3>' in line:
        new_lines.append('<details class="accordion">\n')
        new_lines.append('<summary>👶 Informations générales du bébé</summary>\n')
        new_lines.append('<div class="accordion-content">\n')
        continue
        
    if '<h3>Configuration du Formulaire "Mon Pronostic"</h3>' in line:
        new_lines.append('<details class="accordion" open>\n')
        new_lines.append('<summary>⚙️ Configuration globale (Formulaire, Tableau, Couleurs)</summary>\n')
        new_lines.append('<div class="accordion-content">\n')
        continue
        
    if '<div style="margin-bottom: 3rem;">' in line and 'Barème de points' in lines[i+1]:
        new_lines.append('<details class="accordion">\n')
        new_lines.append('<summary>💯 Barème de points</summary>\n')
        new_lines.append('<div class="accordion-content">\n')
        new_lines.append(line)
        continue
        
    if '<div style="margin-bottom: 3rem;">' in line and 'Indices existants' in lines[i+1]:
        new_lines.append('<details class="accordion">\n')
        new_lines.append('<summary>💡 Gestion des indices</summary>\n')
        new_lines.append('<div class="accordion-content">\n')
        new_lines.append(line)
        continue
        
    if '<hr style="border: 0; height: 1px; background: rgba(0,0,0,0.1); margin-bottom: 2rem;">' in line:
        # Before hr, we need to close the accordion
        if len(new_lines) > 30: # don't do this for the very first ones if any
            new_lines.append('    </div>\n</details>\n')
        continue # skip the hr

    new_lines.append(line)

# Add closing tag for the last section (Indices) before the final </div> of form-container
for i in range(len(new_lines)-1, 0, -1):
    if '</div>' in new_lines[i] and '{% endblock %}' in new_lines[i+1]:
        new_lines.insert(i, '    </div>\n</details>\n')
        break

with open('templates/admin_info.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
